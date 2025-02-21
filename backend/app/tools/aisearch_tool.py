import os
import re
import requests
import urllib.parse
from typing import List, Type
import numpy as np
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
from tenacity import retry, stop_after_attempt, wait_exponential
from app.tools.current_date_tool import CurrentDateTool
from openai import AzureOpenAI

class AISearchInput(BaseModel):
    query: str = Field(..., description="Search query for AI research or user topic")

def serper_search(query: str) -> List[str]:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not set in environment.")
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {"q": query}
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    organic_results = data.get("organic", [])
    links = [result.get("link") for result in organic_results if result.get("link")]
    return links

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
def fetch_reader_content(link: str) -> str:
    reader_url = f"https://r.jina.ai/{urllib.parse.quote(link, safe='')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(reader_url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

def get_embedding(text: str) -> List[float]:
    """
    Uses Azure OpenAI's latest API via the AzureOpenAI client to generate text embeddings.
    Environment variables used:
      - AZURE_OPENAI_API_KEY
      - AZURE_API_VERSION (default "2024-06-01")
      - AZURE_OPENAI_ENDPOINT
      - AZURE_OPENAI_EMBEDDING_MODEL (default "text-embedding-3-large")
    """
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION", "2024-06-01"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    response = client.embeddings.create(
        input=text,
        model=embedding_model
    )
    # Use attribute access instead of subscripting the response
    return response.data[0].embedding

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def filter_relevant_chunks(content: str, query: str, threshold: float = 0.75) -> str:
    """
    Splits the document into paragraphs, embeds each one, and retains only those
    paragraphs that have cosine similarity above the threshold with the query embedding.
    """
    paragraphs = re.split(r'\n\s*\n', content)
    query_emb = get_embedding(query)
    relevant_chunks = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para_emb = get_embedding(para)
        similarity = cosine_similarity(query_emb, para_emb)
        if similarity >= threshold:
            relevant_chunks.append(para)
    return "\n\n".join(relevant_chunks) if relevant_chunks else content[:1000]

class AISearchTool(BaseTool):
    name: str = "aisearch_tool"
    description: str = (
        "Search the web for the latest information relevant to the user's query. "
        "This tool uses the Serper AI API to obtain live search result links and then feeds each link to Jina Reader "
        "to extract content. The extracted text is filtered using embeddings (via Azure OpenAI) so that only the most relevant "
        "portions are retained. The current date is appended to ensure up-to-date context."
    )
    args_schema: Type[BaseModel] = AISearchInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)
    result_as_answer: bool = True

    def _run(self, query: str) -> str:
        print(f"[AISearchTool] Received query: '{query}'")
        # Append the current date from CurrentDateTool
        current_date = CurrentDateTool()._run().strip()
        query = f"{query} {current_date}"
        print(f"[AISearchTool] Final query after appending current date: '{query}'")
        
        print(f"[AISearchTool] Querying Serper AI for: '{query}'")
        try:
            links = serper_search(query)
            if not links:
                return "No search results found from Serper AI."
        except Exception as e:
            return f"Error fetching search links from Serper AI: {e}"
        
        # Limit to a maximum of 15 links.
        links = links[:15]
        print(f"[AISearchTool] Retrieved {len(links)} links from Serper AI.")
        
        combined_contents = []
        print("[AISearchTool] Extracting content using Jina Reader for each link...")
        for link in links:
            try:
                full_content = fetch_reader_content(link)
                # Filter the content: embed each paragraph and select only those relevant to the query.
                relevant_content = filter_relevant_chunks(full_content, query)
                combined_contents.append(f"URL: {link}\nContent:\n{relevant_content}\n{'-'*40}\n")
                print(f"[AISearchTool] Successfully processed content from: {link}")
            except Exception as e:
                combined_contents.append(f"URL: {link}\nError fetching content: {e}\n{'-'*40}\n")
                print(f"[AISearchTool] Error processing {link}: {e}")
        
        final_result = "\n".join(combined_contents)
        return final_result

    async def _arun(self, query: str) -> str:
        return self._run(query)
