# mcp_servers/arxiv/server.py

from mcp.server.fastmcp import FastMCP
import arxiv

arxiv_client = arxiv.Client()

mcp = FastMCP("arxiv-server")

@mcp.tool()
def search_arxiv(query: str, max_results: int = 5, sort_by: str = "relevance"):
    """
    Search for research papers by topic/query
    Returns paper title + authors + url + published date + abstract snippet
    Args: 
        query:        The search query
        max_results:  Maximum number of results to return
        sort_by:     "relevance" or "recent" (default: relevance)
    """

    sort_map = {
        "relevance": arxiv.SortCriterion.Relevance,
        "recent": arxiv.SortCriterion.SubmittedDate
    }

    sort_criterion = sort_map.get(sort_by.lower(), arxiv.SortCriterion.Relevance)

    results = []

    try:
        search = arxiv.Search(query=query, max_results=max_results, sort_by=sort_criterion)
        search_results = arxiv_client.results(search)

        for r in search_results:
            authors_str = ','.join(a.name for a in r.authors)
            paper_id = r.entry_id.split("/")[-1].split("v")[0]  

            results.append(
                f"Title: {r.title}\n"
                f"Authors: {authors_str}\n"
                f"Paper ID: {paper_id}\n"       
                f"URL: {r.entry_id}\n"
                f"PDF: {r.pdf_url}\n"
                f"Updated: {r.updated}\n"
                f"Abstract: {r.summary[:300]}...\n" 
                f"{'─' * 40}"
            )
    except Exception as e:
        return f"Arxiv search failed {e}"
    
    return "\n".join(results) if results else f"No result for {query}"


@mcp.tool()
def get_paper_details(paper_id: str):
    """
    Get full abstract and metadata for a specific paper
    Returns full abstract + authors + categories + published date
    Args:
        paper_id : the arxiv paper ID e.g. "2301.07041"
    """
    try: 
        search = arxiv.Search(id_list=[paper_id])

        result_1 = next(arxiv_client.results(search))

        authors_str = ",".join(a.name for a in result_1.authors)

        categories_str = ",".join(result_1.categories)

        journal_ref = result_1.journal_ref if result_1.journal_ref else "Not published in journal yet"

    
    except Exception as e:
        return f"Failed to get paper details {e}"
    
    return (
                f"Title: {result_1.title}\n"
                f"Authors: {authors_str}\n"
                f"Categories: {categories_str}\n"
                f"URL: {result_1.entry_id}\n"
                f"Updated: {result_1.updated}\n"
                f"Journal: {journal_ref}\n"
                f"Abstract: {result_1.summary}...\n" 
                f"{'─' * 40}"
                )

if __name__ == "__main__":
    mcp.run()