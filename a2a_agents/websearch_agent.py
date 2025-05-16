from a2a_servers.common.server.server import A2AServer
from python_a2a import A2AServer, skill, agent, run_server, TaskStatus, TaskState
from mcp import ClientSession, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio

@agent(
    name="Web Search Agent",
    description="Performs web searches using DuckDuckGo",
    version="1.0.0"
)
class WebSearchAgent(A2AServer):
    def __init__(self):
        self.tools = None
        asyncio.run(self.initialize_tools())

    async def initialize_tools(self):
        server_params = StdioServerParameters(
            command="python",
            args=["websearch_server.py"],
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.tools = await load_mcp_tools(session)

    @skill(
        name="Web Search",
        description="Perform a web search using DuckDuckGo",
        tags=["search", "information"]
    )
    async def web_search(self, query: str) -> str:
        """Perform a web search and return results"""
        if not self.tools:
            raise ValueError("Tools not initialized")
        return await self.tools[0].run(query)

    async def handle_task(self, task):
        message_data = task.message or {}
        content = message_data.get("content", {})
        query = content.get("text", "") if isinstance(content, dict) else ""

        if not query:
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={"role": "agent", "content": {"type": "text", 
                         "text": "Please provide a search query."}}
            )
            return task

        try:
            results = await self.web_search(query)
            task.artifacts = [{
                "parts": [{"type": "text", "text": results}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        except Exception as e:
            task.status = TaskStatus(
                state=TaskState.FAILED,
                message={"role": "agent", "content": {"type": "text", 
                         "text": f"Search failed: {str(e)}"}}
            )
        
        return task

if __name__ == "__main__":
    agent = WebSearchAgent()
    run_server(agent, port=5001)