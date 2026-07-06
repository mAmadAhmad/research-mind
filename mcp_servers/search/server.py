# mcp_servers/search/server.py

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from tavily import TavilyClient

load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=api_key)

mcp = FastMCP("search-server")



@mcp.tool()
def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the open web for a given query.
    Returns titles, URLs and snippets of top results.

    Args:
        query: The search query
        max_results: Maximum number of results to return
    """
    result = []
    try:
        response = tavily_client.search(query=query, max_results=max_results, search_depth='basic')
        for res in response["results"]:
            result.append(f"{res['content']} : {res['url']}")
    except Exception as e:
        return(f"Search failed {e}")
    
    return "\n".join(result) if result else f"No result for {query}"



if __name__ == "__main__":
    mcp.run()