from mcp.server.fastmcp import FastMCP
from smolagents import DuckDuckGoSearchTool

mcp = FastMCP("websearch_server")

@mcp.tool()
def web_search(query: str) -> str:
    """
    Perform a DuckDuckGo web search for a given natural language query.

    Input:
        query (str): A search string describing what information to retrieve from the web.
            Examples:
                - "Latest news on artificial general intelligence in 2025"
                - "Top 5 Python libraries for data visualization"
                - "Recent breakthroughs in battery technology"

    Output:
        List[str]: A list of up to 5 textual summaries or snippet results found for the query.
            Each result is a short snippet of content returned by the DuckDuckGo search engine.

    Use Cases:
        - Fetching recent news or updates on a topic
        - Performing open-domain question answering from public web content
        - Quickly gathering external context or definitions

    Notes:
        - This tool does not provide URLs, only the result snippets.
        - Intended for fast, privacy-preserving web lookups (DuckDuckGo).
        - Results may be approximate and should be verified for factual accuracy if critical.
    """
    search_tool = DuckDuckGoSearchTool()
    return search_tool.run(query)

if __name__ == "__main__":
    mcp.run(transport="stdio")