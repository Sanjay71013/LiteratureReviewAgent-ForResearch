import arxiv
import asyncio
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import List, TypedDict, Annotated

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

import os
import getpass

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# Defining the state

class State(TypedDict):
    messages: Annotated[list, add_messages]

# async def initialize_agent_resources():
#     server_params = StdioServerParameters(
#     command="python",
#     # Make sure to update to the full absolute path to your math_server.py file
#     args=["agents/research_server.py"],
#     )

#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             # Initialize the connection
#             await session.initialize()

#             # Get tools
#             tools = await load_mcp_tools(session)

#             return tools

# tools = asyncio.run(initialize_agent_resources())

# # Initializing components
# llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14", temperature=0)
# llm_with_tools = llm.bind_tools(tools)
# tool_node = ToolNode(tools=tools)

# # Creating agent prompt
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You're a helpful assistant for academic research. When asked to find papers and summarize them, first use arxiv_search to find the papers. Then, for each paper found, present its title, authors, and publication date. After presenting this metadata, use the summarize_text tool to summarize its abstract (the 'summary' field from arxiv_search). Present the summary of each paper clearly. Ensure you process all papers found before concluding."),
#     MessagesPlaceholder("messages"),
# ])

# # Building the graph
# async def agent(state: State):
#     return {"messages": [llm_with_tools.invoke(state["messages"])]}

# workflow = StateGraph(State)

# workflow.add_node("agent", agent)
# workflow.add_node("tools", tool_node)
# workflow.add_conditional_edges(
#     "agent",
#     tools_condition
# )
# workflow.add_edge("tools", "agent")
# workflow.set_entry_point("agent")
# memory = MemorySaver()
# graph = workflow.compile(checkpointer=memory)

# # Usage example

# # User message
# user_input = "Find recent papers on quantum machine learning and summarize them."

# config = {"configurable": {"thread_id": "1"}}


# async def run_async_graph():
#     events = graph.astream(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": user_input,
#                 },
#             ],
#         },
#         config,
#         stream_mode="values",
#     )
#     async for event in events:
#         if "messages" in event:
#             event["messages"][-1].pretty_print()


# asyncio.run(run_async_graph())


async def main():
    # Initialize MCP tools and keep session open
    server_params = StdioServerParameters(
        command="python",
        args=["agents/research_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)

            # Bind LLM with tools
            llm = ChatOpenAI(model="gpt-4.1-nano-2025-04-14", temperature=0)
            llm_with_tools = llm.bind_tools(tools)
            tool_node = ToolNode(tools=tools)

            # Define agent
            async def agent(state: State):
                response = await llm_with_tools.ainvoke(state["messages"])
                return {"messages": [response]}

            # Create prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You're a helpful assistant for academic research. When asked to find papers and summarize them, first use arxiv_search to find the papers. Then, for each paper found, present its title, authors, and publication date. After presenting this metadata, use the summarize_text tool to summarize its abstract (the 'summary' field from arxiv_search). Present the summary of each paper clearly. Ensure you process all papers found before concluding."),
                MessagesPlaceholder("messages"),
            ])

            # Build workflow
            workflow = StateGraph(State)
            workflow.add_node("agent", agent)
            workflow.add_node("tools", tool_node)
            workflow.add_conditional_edges("agent", tools_condition)
            workflow.add_edge("tools", "agent")
            workflow.set_entry_point("agent")
            memory = MemorySaver()
            graph = workflow.compile(checkpointer=memory)

            # Run the graph with input
            user_input = "Find recent papers on quantum machine learning and summarize them."
            config = {"configurable": {"thread_id": "1"}}

            events = graph.astream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        },
                    ],
                },
                config,
                stream_mode="values",
            )

            async for event in events:
                if "messages" in event:
                    event["messages"][-1].pretty_print()

# Run it
if __name__ == "__main__":
    asyncio.run(main())
