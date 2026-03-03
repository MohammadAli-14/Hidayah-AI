"""
Hidayah AI — Web Search Tool
Wraps the Tavily API for fetching scholarly Islamic content from the web.
"""

from utils.config import TAVILY_API_KEY
from utils.logger import get_logger

log = get_logger("web_search")


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web using Tavily API.
    Returns a list of result dicts: [{"title": ..., "url": ..., "content": ...}, ...]
    """
    if not TAVILY_API_KEY:
        log.warning("Tavily API Key Missing - Bypassing web search.")
        return [{"title": "API Key Missing", "url": "", "content": "Tavily API key not configured. Please add TAVILY_API_KEY to your .env file."}]

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=TAVILY_API_KEY)

        log.info(f"Searching web for: '{query[:80]}'")
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=True,
        )

        results = []

        # Include the AI-generated answer if available
        if response.get("answer"):
            results.append({
                "title": "Tavily Summary",
                "url": "",
                "content": response["answer"],
            })

        # Include individual search results
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            })

        log.info(f"Found {len(results)} distinct sources.")
        return results

    except Exception as e:
        log.error(f"Search failed: {e}")
        return [{"title": "Search Error", "url": "", "content": f"Web search failed: {str(e)}"}]
