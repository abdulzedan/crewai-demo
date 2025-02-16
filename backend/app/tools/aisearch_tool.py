# backend/app/tools/aisearch_tool.py

from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
import os
import re
import requests
import bs4  # BeautifulSoup for HTML parsing
from app.tools.current_date_tool import CurrentDateTool
from app.services.custom_memory_manager import CustomMemoryManager

class AISearchInput(BaseModel):
    query: str = Field(..., description="Search query for AI research")

class AISearchTool(BaseTool):
    name: str = "ai_search_tool"
    description: str = (
        "Search the web for the latest AI research articles and news. "
        "If a year is not provided in the query, today's date will be appended. "
        "Only results whose full content mentions today's date are returned."
    )
    args_schema: Type[BaseModel] = AISearchInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        # Append today's date if the query does not contain a 4-digit year.
        if not re.search(r'\b\d{4}\b', query):
            current_date = CurrentDateTool()._run()  # e.g., "2025-02-15"
            query += f" {current_date}"
        else:
            current_date = CurrentDateTool()._run()
        
        # Use the Serper API to perform a real web search.
        serper_api_key = os.getenv("SERPER_API_KEY", "")
        if not serper_api_key:
            raise ValueError("SERPER_API_KEY not set in environment.")
        
        # Updated URL per documentation.
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {"q": query}
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(
                f"Web search API request failed with status code {response.status_code}: {response.text}"
            )
        
        data = response.json()
        organic_results = data.get("organic", [])
        if not organic_results:
            return "No results found."
        
        result_str = f"Web search results (filtered for content mentioning '{current_date}'):\n\n"
        count = 0
        for result in organic_results:
            if count >= 10:
                break
            title = result.get("title", "No title")
            link = result.get("link", "No link")
            snippet = result.get("snippet", "No snippet")
            
            # Fetch full page content.
            try:
                page_response = requests.get(link, timeout=5)
                if page_response.status_code == 200:
                    soup = bs4.BeautifulSoup(page_response.text, 'html.parser')
                    full_text = soup.get_text(separator="\n")
                    # Filter: include only if the content mentions the current date.
                    if current_date not in full_text:
                        continue
                    preview = full_text[:500].strip() + "..."
                else:
                    preview = "Unable to fetch full content."
            except Exception as e:
                preview = f"Error fetching content: {e}"
            
            result_str += (
                f"{count+1}. **{title}**\n"
                f"   - **Link:** {link}\n"
                f"   - **Snippet:** {snippet}\n"
                f"   - **Content Preview:** {preview}\n\n"
            )
            count += 1

        if count == 0:
            result_str += "No results found that mention today's date in their content.\n"

        # Store the result in short-term memory.
        try:
            memory_manager = CustomMemoryManager(persist_dir=".chroma-local")
            memory_manager.add_memory(result_str)
        except Exception as mem_err:
            print("Error storing to short term memory:", mem_err)

        return result_str

    async def _arun(self, query: str) -> str:
        return self._run(query)
