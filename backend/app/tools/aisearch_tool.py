import concurrent.futures
import os
import re
import urllib.parse

import numpy as np
import requests
from crewai.tools import BaseTool
from openai import AzureOpenAI
from pydantic import BaseModel, ConfigDict, Field
from tenacity import retry, stop_after_attempt, wait_exponential

from app.tools.current_date_tool import CurrentDateTool


# Input model now includes a dynamic max_links field.
class AISearchInput(BaseModel):
    query: str = Field(..., description="Search query for AI research or user topic")
    max_links: int = Field(3, description="Maximum number of links to retrieve from search")


def serper_search(query: str) -> list[dict]:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY not set in environment.")
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = {"q": query}
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    organic_results = data.get("organic", [])
    results = []
    for result in organic_results:
        link = result.get("link")
        if link:
            results.append(
                {
                    "url": link,
                    "title": result.get("title", "No Title"),
                    "snippet": result.get("snippet", "No Snippet"),
                }
            )
    return results


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
def fetch_reader_content(link: str) -> str:
    reader_url = f"https://r.jina.ai/{urllib.parse.quote(link, safe='')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(reader_url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def filter_relevant_chunks(content: str, query: str, threshold: float = 0.75, max_paragraphs: int = 20) -> str:
    # Remove markdown images and extraneous lines (e.g., "URL Source:" and "Image <number>")
    content = re.sub(r"!\[.*?\]\(.*?\)", "", content)
    content = re.sub(r"URL Source:\s*https?:\/\/\S+", "", content)
    content = re.sub(r"Image\s+\d+.*", "", content)

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
    if len(paragraphs) > max_paragraphs:
        paragraphs = paragraphs[:max_paragraphs]

    query_emb = get_embedding(query)
    para_embs = get_embedding(paragraphs)
    relevant_chunks = []
    for para, emb in zip(paragraphs, para_embs):
        similarity = cosine_similarity(query_emb, emb)
        if similarity >= threshold:
            relevant_chunks.append(para)
    return "\n\n".join(relevant_chunks) if relevant_chunks else content[:1000]


def get_embedding(text: str | list[str]) -> list[float] | list[list[float]]:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION", "2024-06-01"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    if isinstance(text, list):
        response = client.embeddings.create(input=text, model=embedding_model)
        return [item.embedding for item in response.data]
    else:
        response = client.embeddings.create(input=[text], model=embedding_model)
        return response.data[0].embedding


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class AISearchTool(BaseTool):
    name: str = "aisearch_tool"
    description: str = (
        "Search the web for the latest information relevant to the user's query. "
        "This tool uses the Serper AI API to obtain live search result links and then "
        "feeds each link to Jina Reader to extract content. "
        "The extracted text is filtered using embeddings (via Azure OpenAI) so that "
        "only the most relevant portions are retained. "
        "The current date is appended to ensure up-to-date context."
    )
    args_schema: type[BaseModel] = AISearchInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)
    result_as_answer: bool = True

    def _run(self, query: str, max_links: int = 3) -> str:
        print(f"[AISearchTool] Received query: '{query}' with max_links={max_links}")
        current_date = CurrentDateTool()._run().strip()
        query = f"{query} {current_date}"
        print(f"[AISearchTool] Final query after appending current date: '{query}'")

        try:
            results = serper_search(query)
            if not results:
                return "No search results found from Serper AI."
        except Exception as e:
            return f"Error fetching search links from Serper AI: {e}"

        # Limit results based on the provided max_links value.
        results = results[:max_links]
        print(f"[AISearchTool] Retrieved {len(results)} links from Serper AI.")

        combined_contents = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(results)) as executor:
            future_to_result = {executor.submit(fetch_reader_content, res["url"]): res for res in results}
            for future in concurrent.futures.as_completed(future_to_result):
                res = future_to_result[future]
                try:
                    full_content = future.result()
                    relevant_content = filter_relevant_chunks(full_content, query, max_paragraphs=20)
                    combined_contents.append(
                        f"URL: {res['url']} | Title: {res['title']} | Snippet: {res['snippet']}\nContent:\n{relevant_content}\n{'-'*40}\n"
                    )
                except Exception as e:
                    combined_contents.append(f"URL: {res['url']}\nError fetching content: {e}\n{'-'*40}\n")
        # Prepend a header with all search link information so it is present in the output.
        header = "\n".join(
            [f"URL: {res['url']} | Title: {res['title']} | Snippet: {res['snippet']}" for res in results]
        )
        self.search_links = results
        final_result = header + "\n" + "\n".join(combined_contents)
        return final_result

    async def _arun(self, query: str, max_links: int = 3) -> str:
        return self._run(query, max_links)
