import os
os.environ["SERPER_API_KEY"] = "1870ff3ce26db44853ad7478e8ee18293080661c"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-9Bvz0fdqJO8C6yX7O6nfT3BlbkFJVuHTEZZodE9zTeqzCRIO"

from crewai import Agent
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Senior Researcher',
  goal='Find real world data to build market sizing models',
  verbose=True,
  memory=True,
  max_iter=10,
  backstory=(
    "Driven by the commitment to getting a good estimate of the true market size for a startup."
    "You do not calculate TAM as a percentage of a total industry size. Rather, you find an estimated number of world wide users x the price of the product."
    "You understand that despite the challenges and uncertainties, you must come up with an estimated final, single answer for TAM."
    "You understand that you will never get a perfect internet answer, so we must make assumptions."
  ),
  tools=[search_tool],
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Deliver a one paragraph summary of the researcher agent findings including a best guess for TAM (Total Addressable Market) for the provided startup.',
  verbose=True,
  memory=True,
  max_iter=3,
  backstory=(
    "Devoid of emotion, only interested in delivering the most accurate report possible."
    "Able to guess and make calculated predictions when necessary to save time."
  ),
  tools=[search_tool],
  allow_delegation=False
)

from crewai import Task

# Research task
research_task = Task(
  description=(
    "Learn about various startup market sizing frameworks and formulas."
    "Learn about the startup, {topic}. Visit their website and ensure you find information related to product pricing."
    "Conduct the market sizing analysis."
    "Final report includes everything the writer agent needs to deliver an accurate assessment of the startup's TAM, including a final guess."
  ),
  expected_output='Estimate for TAM',
  tools=[search_tool],
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Briefly organize the information compiled by the research agent."
    "Provide a final TAM estimate for the startup in $USD."
  ),
  expected_output='A final market sizing calculation and report.',
  tools=[search_tool],
  agent=writer,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)

from crewai import Crew, Process

# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'Taskade'})
print(result) 