from mcp.server.fastmcp import FastMCP
import arxiv
from langchain_openai import ChatOpenAI
from typing import List

mcp = FastMCP("research_server")

@mcp.tool()
def arxiv_search(query: str) -> List[dict]:
    """Search arXiv for academic papers matching a query.
    
    Args:
        query: A search string containing keywords/phrases to find in paper titles/abstracts.
            Example: "quantum machine learning" or "attention mechanisms in transformers".
    
    Returns:
        List[dict]: A list of dictionaries containing paper metadata (title, authors, summary, 
        publication date, and comments) for up to 3 most relevant recent papers.
    """
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=3, sort_by=arxiv.SortCriterion.SubmittedDate)
    return [{
        "title": result.title,
        "authors": [author.name for author in result.authors],
        "summary": result.summary,
        "published": str(result.published),
        "comments": result.comment,
    } for result in client.results(search)]

@mcp.tool()
def summarize_text(text: str) -> str:
    """Generate a concise summary of text content using an LLM.
    
    Args:
        text: The content to summarize. Can be plain text up to 4000 characters.
            Example: A research paper abstract or technical article content.
    
    Returns:
        str: A condensed version preserving key information and main points,
        typically 1-3 paragraphs long depending on input length.
    """
    llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14", temperature=0)
    return llm.predict(f"Summarize this text concisely:\n\n{text}").content


if __name__ == "__main__":
    mcp.run(transport="stdio")