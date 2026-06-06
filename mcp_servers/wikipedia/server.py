# mcp_servers/wikipedia/server.py

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wikipedia-server")

# Tools
@mcp.tool()
def search_wikipedia(topic: str, max_results: int = 5) -> str:
    """
    Search Wikipedia for articles related to a topic.
    Returns a list of article titles and URLs.
    
    Args:
        topic: The topic to search for
        max_results: Maximum number of results to return
    """
    import wikipedia

    search_results = wikipedia.search(query=topic, results=max_results)
    results = []
    for result in search_results:
        try: 
            url = wikipedia.page(result).url
            results.append(f"{result}: {url}")
        except wikipedia.exceptions.DisambiguationError:
            continue
        except wikipedia.exceptions.PageError:
            continue
    
    return "\n".join(results) if results else "No articles found for {topic}"


@mcp.tool()
def get_wikipedia_summary(article_title: str) -> str:
    """
    Get the summary/intro section of a specific Wikipedia article.
    
    Args:
        article_title: Exact or approximate title of the Wikipedia article
    """
    import wikipediaapi

    wiki = wikipediaapi.Wikipedia('research_mind/1.0 (amadj8223@gmail.com)', 'en')
    page = wiki.page(title=article_title)

    if not page.exists():
        return f"No article found for {article_title}"
    
    return page.summary

if __name__ == "__main__":
    mcp.run()