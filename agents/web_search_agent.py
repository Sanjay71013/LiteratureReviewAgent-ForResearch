from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, ToolCollection, tool
from mcp import ClientSession, StdioServerParameters
from dotenv import load_dotenv
import os

load_dotenv()

# API key
api_key = os.getenv('HUGGING_FACE_API_KEY')

server_params = StdioServerParameters(
        command="python",
        args=["agents/websearch_server.py"],
    )

with ToolCollection.from_mcp(server_params, trust_remote_code=True) as tool_collection:
    tools = [*tool_collection.tools]

# Initializing the model
model = HfApiModel(token=api_key)

# Creating the agent
agent = CodeAgent(tools=tools, model=model)

# Running the agent with a query
response = agent.run("Last 5 uefa world cup champions")
print(response)
