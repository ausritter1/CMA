import os
import pandas as pd
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Set environment variables for API keys
os.environ["SERPER_API_KEY"] = "1870ff3ce26db44853ad7478e8ee18293080661c"
os.environ["OPENAI_API_KEY"] = "sk-proj-9Bvz0fdqJO8C6yX7O6nfT3BlbkFJVuHTEZZodE9zTeqzCRIO"

# Load the CSV file
csv_path = "VC_Deals_Data.csv"
df = pd.read_csv(csv_path)

# Create a senior researcher agent with memory and verbose mode
search_tool = SerperDevTool()
researcher = Agent(
  role='Senior Researcher',
  goal='Find data to fill in the gaps in my spreadsheet on recent startup fundings.',
  verbose=True,
  memory=True,
  max_iter=5,
  backstory=(
    "You are a web researcher agent built to find missing recent startup deal funding information from the provided CSV file."
  ),
  tools=[search_tool],
  allow_delegation=True
)

# Create a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Return the completed CSV file with all cells filled out.',
  verbose=True,
  memory=True,
  max_iter=2,
  backstory=(
    "You are a writer agent built to take the research from the researcher agent and return the completed file."
  ),
  tools=[search_tool],
  allow_delegation=False
)

# Define research task
research_task = Task(
  description=(
    "Search the web for missing startup deal funding information from the CSV file. Input the CSV data, find missing fields, and return the updated data."
  ),
  expected_output='Missing cell data',
  tools=[search_tool],
  agent=researcher,
  input_data={'csv_data': df.to_dict()},
)

# Define writing task
write_task = Task(
  description=(
    "Organize the information compiled by the research agent into a CSV in the same format as the input."
  ),
  expected_output='A final completed CSV file or text.',
  tools=[search_tool],
  agent=writer,
  async_execution=False,
  input_data={'csv_data': df.to_dict()},
  output_file='Completed_VC_Deals_Data.csv'  # Save the completed CSV file
)

# Form the tech-focused crew
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential,
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

# Start the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': csv_path})
print(result)

# Save the result if it is a completed CSV data
if 'completed_csv' in result:
    completed_df = pd.DataFrame(result['completed_csv'])
    completed_df.to_csv('Completed_VC_Deals_Data.csv', index=False)
