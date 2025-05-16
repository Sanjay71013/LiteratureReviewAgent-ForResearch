import os
import time
import litellm
from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    FileWriterTool,
)
from datetime import datetime

def print_time_taken(time_taken):
    """Prints the time taken to execute the crew."""
    print("\n" + "-" * 50 + "\n")
    if time_taken < 60:
        print("Time taken to execute crew: less than 1 minute")
    else:
        print(f"Time taken to execute crew: {time_taken / 60:.2f} minutes")
    print("\n" + "-" * 50 + "\n")

# Configure Azure OpenAI access
os.environ.update({
    "AZURE_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
    "AZURE_API_BASE": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "AZURE_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION"),
    "LITELLM_LOG": 'DEBUG',
})

litellm.set_verbose=False

# Setup file paths
current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
script_name = os.path.splitext(os.path.basename(__file__))[0]
root_folder_path = 'c:\\CrewAI'
output_folder_path = os.path.join(root_folder_path, f"{script_name}_{current_date}")
os.makedirs(output_folder_path, exist_ok=True)  # Create the output folder if it doesn't exist

# Initialize the tool

# Write the result to a file with UTF-8 encoding to handle special characters
input_args = {
    'filename': f"Report_{current_date}.txt",
    'content': "test",
    'directory': output_folder_path,
    'overwrite': True,
    'encoding': 'utf-8'
}


file_writer_tool = FileWriterTool()
file_writer_tool2 = FileWriterTool(directory=output_folder_path)

start_time = time.time()

# Create an Agent instance with the specified role, goal, and backstory
txt_agent = Agent(
    role='Thinker',  # Role of the agent
    goal='think about python',  # Goal
    backstory=(
        "Excelent thinker."
    ),  
    llm = "azure/gpt4o",
    tools=[file_writer_tool],  # TXT tool required for this task
    verbose=True,  # Verbose output setting
)

# Define the task: reading and displaying the TXT content
task1 = Task(
    description="Write Python versions list to a file.",  # Task description
    expected_output="Save to file a plain text data.",  # Expected output format
    agent=txt_agent,  # Agent assigned to the task
    max_iterations=3,  # Maximum number of iterations allowed
    async_execution=False,  # Synchronous execution
    context=None,  # No additional context provided    
    output_pydantic=None,  # No Pydantic model specified for output
    step_callback=None,  # No step callback
    task_callback=None,  # No task callback
    allow_delegation=False,  # Delegation not allowed
    human_input=False,  # No human input required    
)

# Create a Crew instance with the defined agent and task
crew = Crew(
    agents=[txt_agent],  # List of agents
    tasks=[task1],  # List of tasks
    full_output=False,  # Full output setting
    process=Process.sequential,  # Process flow
    memory=False,  # Enable memory usage
    cache=False,  # Enable caching
    embedder=None,  # No embedder specified
    step_callback=None,  # No step callback
    task_callback=None,  # No task callback
    share_crew=False,  # Do not share crew information
    #output_log_file="output_Crew_txt.txt",  # Output log file set to "output_Crew_txt.txt"
    verbose=True  # Verbose output setting
)

# Kick off the crew to start executing the task
result = crew.kickoff()

# Print the final output (assuming it contains the most relevant information)
print(result)
print("\n" + "-"*50 + "\n")

input_args = {
    'filename': "test.txt",
    'content': "test content",
    'directory': "c:\\temp",
    'overwrite': True,
    'encoding': 'utf-8'
}
file_writer_tool._run(** input_args)

# Print the usage metrics of the crew
print(crew.usage_metrics)
print("\n" + "-" * 50 + "\n")

# Print the time taken to execute the task
end_time = time.time()
print_time_taken(end_time - start_time)