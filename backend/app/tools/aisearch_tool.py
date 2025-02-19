# backend/app/tools/aisearch_tool.py

from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
import os
import re
import requests
import bs4
from playwright.sync_api import sync_playwright
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime
import dateparser.search

class AISearchInput(BaseModel):
    query: str = Field(..., description="Search query for AI research or user topic")

def extract_text_from_html(html: str) -> str:
    """Extract text from HTML, focusing on main content if available."""
    soup = bs4.BeautifulSoup(html, 'html.parser')
    main_content = soup.find('article') or soup.find('main') or soup.body
    if main_content:
        return main_content.get_text(separator="\n", strip=True)
    return soup.get_text(separator="\n", strip=True)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
def get_page_content(url: str) -> str:
    """Fetch full page content using Playwright, but with a shorter timeout."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        )
        # Shorter timeout and only wait for 'domcontentloaded' instead of 'networkidle'
        page.goto(url, timeout=8000, wait_until="domcontentloaded")
        content = page.content()
        browser.close()
        return content

class AISearchTool(BaseTool):
    name: str = "ai_search_tool"
    description: str = (
        "Search the web for the latest information relevant to the user's query. "
        "Use only if the user input requires external data or references."
    )
    args_schema: Type[BaseModel] = AISearchInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        """
        Perform a web search. For demonstration, we simulate a search by fetching
        content from a placeholder URL.
        """
        # Replace this with your actual search logic or API call if available.
        example_url = "https://example.com"
        try:
            html = get_page_content(example_url)
            full_text = extract_text_from_html(html)
            # For brevity, return a snippet of the content.
            return "Simulated search results:\n\n" + full_text[:300] + "..."
        except Exception as e:
            return f"Error in AISearchTool: {e}"

    async def _arun(self, query: str) -> str:
        return self._run(query)


# SLOWER IMPLEMENTATION
# # backend/app/tools/aisearch_tool.py

# from typing import Type
# from pydantic import BaseModel, Field, ConfigDict
# from crewai.tools import BaseTool
# import os
# import re
# import requests
# import bs4  # BeautifulSoup for HTML parsing
# from datetime import datetime
# import dateparser.search
# from playwright.sync_api import sync_playwright
# from tenacity import retry, stop_after_attempt, wait_exponential
# from app.tools.current_date_tool import CurrentDateTool
# from app.services.custom_memory_manager import CustomMemoryManager

# class AISearchInput(BaseModel):
#     query: str = Field(..., description="Search query for AI research")

# @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
# def get_page_content(url: str) -> str:
#     """Fetch full page content using Playwright to bypass anti-scraping measures."""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page(
#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/91.0.4472.124 Safari/537.36"
#             )
#         )
#         page.goto(url, timeout=3000)
#         # Wait for network to be idle if necessary (adjust as needed)
#         page.wait_for_load_state("networkidle")
#         content = page.content()
#         browser.close()
#         return content

# def extract_text_from_html(html: str) -> str:
#     """Extract text from HTML, focusing on main content if available."""
#     soup = bs4.BeautifulSoup(html, 'html.parser')
#     main_content = soup.find('article') or soup.find('main') or soup.body
#     if main_content:
#         return main_content.get_text(separator="\n", strip=True)
#     return soup.get_text(separator="\n", strip=True)

# def is_recent_content(text: str, max_days_old: int = 1) -> bool:
#     """Determine if any dates found in the text are within max_days_old of today."""
#     today = datetime.now().date()
#     # dateparser.search.search_dates returns a list of (string, datetime) tuples
#     results = dateparser.search.search_dates(text)
#     if not results:
#         return False
#     for _, dt in results:
#         if isinstance(dt, datetime) and (today - dt.date()).days <= max_days_old:
#             return True
#     return False

# class AISearchTool(BaseTool):
#     name: str = "ai_search_tool"
#     description: str = (
#         "Search the web for the latest AI research articles and news. "
#         "If a year is not provided in the query, today's date will be appended. "
#         "This tool fetches full content using a headless browser and returns only results "
#         "whose content includes today's date."
#     )
#     args_schema: Type[BaseModel] = AISearchInput
#     model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

#     def _run(self, query: str) -> str:
#         # Append today's date if no 4-digit year is in the query.
#         current_date = CurrentDateTool()._run()  # e.g., "2025-02-15"
#         if not re.search(r'\b\d{4}\b', query):
#             query += f" {current_date}"
        
#         serper_api_key = os.getenv("SERPER_API_KEY", "")
#         if not serper_api_key:
#             raise ValueError("SERPER_API_KEY not set in environment.")
        
#         url = "https://google.serper.dev/search"
#         headers = {
#             "X-API-KEY": serper_api_key,
#             "Content-Type": "application/json"
#         }
#         payload = {"q": query}
        
#         response = requests.post(url, headers=headers, json=payload)
#         if response.status_code != 200:
#             raise Exception(
#                 f"Web search API request failed with status code {response.status_code}: {response.text}"
#             )
        
#         data = response.json()
#         organic_results = data.get("organic", [])
#         if not organic_results:
#             return "No results found."
        
#         result_str = f"Web search results (filtered for content mentioning '{current_date}'):\n\n"
#         count = 0
#         for result in organic_results:
#             if count >= 10:
#                 break
#             title = result.get("title", "No title")
#             link = result.get("link", "No link")
#             snippet = result.get("snippet", "No snippet")
            
#             try:
#                 html = get_page_content(link)
#                 full_text = extract_text_from_html(html)
#                 # Only include result if its content contains today's date.
#                 if not is_recent_content(full_text, max_days_old=1):
#                     continue
#                 preview = full_text[:500].strip() + "..."
#             except Exception as e:
#                 preview = f"Error fetching content: {e}"
            
#             result_str += (
#                 f"{count+1}. **{title}**\n"
#                 f"   - **Link:** {link}\n"
#                 f"   - **Snippet:** {snippet}\n"
#                 f"   - **Content Preview:** {preview}\n\n"
#             )
#             count += 1
        
#         if count == 0:
#             result_str += "No recent results found that mention today's date in their content.\n"
        
#         # Store the result in short-term memory.
#         try:
#             memory_manager = CustomMemoryManager(persist_dir=".chroma-local")
#             memory_manager.add_memory(result_str)
#         except Exception as mem_err:
#             print("Error storing to short term memory:", mem_err)
        
#         return result_str

#     async def _arun(self, query: str) -> str:
#         return self._run(query)
