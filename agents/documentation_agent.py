from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileWriterTool
import os
import getpass

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# Initialize the FileWriterTool
file_writer_tool = FileWriterTool()

llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.8,
    max_tokens=150,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42
)

# Define the agent
documentation_agent = Agent(
    role="Documentation Specialist",
    goal="Compile and format research summaries into a structured document (a txt file).",
    backstory="An expert in creating clear and concise research summaires and document them.",
    llm=llm,
    tools=[file_writer_tool]
)

# Define the task
documentation_task = Task(
    description="Compile the provided research summaries into a structured document and save it to 'literature_review.txt'.",
    expected_output="A well-formatted document containing the research summaries with title of the paper, summary with 100  words for each paper saved to 'literature_review.txt'.",
    agent=documentation_agent,
    output_file="literature_review.docx",
)

# Create the crew
crew = Crew(
    agents=[documentation_agent],
    tasks=[documentation_task],
    verbose=True
)

# Execute the crew
result = crew.kickoff()

print(result)