import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults
from src.tools.base import BaseTool
from src.core.config import settings


class WebSearchInput(BaseModel):
    query: str = Field(description="The search query to look up on the internet")
    max_results: int = Field(default=5, description="Maximum number of results to return")


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Searches the internet for current information, news, and facts."
    args_schema = WebSearchInput
    requires_api_key = True

    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        if self.api_key:
            os.environ["TAVILY_API_KEY"] = self.api_key
            self.tool = TavilySearchResults(max_results=5)
        else:
            self.tool = None

    async def _run(self, query: str, max_results: int = 5) -> str:
        if not self.tool:
            return "Web search is disabled. Missing Tavily API key."
            
        self.tool.max_results = max_results
        try:
            results = await self.tool.ainvoke({"query": query})
            
            if not results:
                return "No results found."
                
            formatted_results = []
            for r in results:
                title = r.get("title", "")
                url = r.get("url", "")
                content = r.get("content", "")
                formatted_results.append(f"Source: {title} ({url})\nContent: {content}\n")
                
            return "\n".join(formatted_results)
        except Exception as e:
            return f"Search failed: {str(e)}"
