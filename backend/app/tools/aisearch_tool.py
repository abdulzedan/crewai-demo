import os
import re
import requests
import urllib.parse
from typing import List, Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
from tenacity import retry, stop_after_attempt, wait_exponential
from app.tools.current_date_tool import CurrentDateTool

class AISearchInput(BaseModel):
    query: str = Field(..., description="Search query for AI research or user topic")

def serper_search(query: str) -> List[str]:
    """
    Calls the Serper AI API to fetch live search result links.
    Returns a list of URLs from the organic results.
    """
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
    """
    Uses Jina Reader to fetch and extract clean content from the given link.
    Prepends 'https://r.jina.ai/' to the URL and adds a User-Agent header.
    """
    reader_url = f"https://r.jina.ai/{urllib.parse.quote(link, safe='')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(reader_url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

class AISearchTool(BaseTool):
    # Name must exactly match the YAML and registry key.
    name: str = "aisearch_tool"
    description: str = (
        "Search the web for the latest information relevant to the user's query. "
        "This tool uses the Serper AI API to obtain live search result links and then feeds each link to Jina Reader "
        "by prepending 'https://r.jina.ai/' to extract clean, LLM-friendly content. "
        "If the query does not contain a four-digit year, today's date is appended."
    )
    args_schema: Type[BaseModel] = AISearchInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)
    # Force the tool output as the final answer so that the agent does not reword the query.
    result_as_answer: bool = True

    def _run(self, query: str) -> str:
        print(f"[AISearchTool] Received query: '{query}'")
        # Append current date if query lacks a four-digit year.
        if not re.search(r'\b\d{4}\b', query):
            current_date = CurrentDateTool()._run().strip()
            query = f"{query} {current_date}"
            print(f"[AISearchTool] Appended current date, updated query: '{query}'")
        
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
        
        # Use Jina Reader to fetch content from each link.
        combined_contents = []
        print("[AISearchTool] Extracting content using Jina Reader for each link...")
        for link in links:
            try:
                content = fetch_reader_content(link)
                combined_contents.append(f"URL: {link}\nContent:\n{content}\n{'-'*40}\n")
                print(f"[AISearchTool] Successfully extracted content from: {link}")
            except Exception as e:
                combined_contents.append(f"URL: {link}\nError fetching content: {e}\n{'-'*40}\n")
                print(f"[AISearchTool] Error extracting content from {link}: {e}")
        
        final_result = "\n".join(combined_contents)
        return final_result

    async def _arun(self, query: str) -> str:
        return self._run(query)
