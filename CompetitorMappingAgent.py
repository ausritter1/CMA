import os
os.environ["SERPER_API_KEY"] = "Your Key Here"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "Your Key Here"

from crewai import Agent
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Senior Researcher',
  goal='Identify and map out the competitive landscape for a given startup or industry.',
  verbose=True,
  memory=True,
  max_iter=10,
  backstory=(
    "You are dedicated to finding startups that operate in the same or related space as the target company."
    "Your goal is to understand the competitive landscape by analyzing competitors' business models, strengths, weaknesses, and market positioning."
    "You explore multiple data sources including public databases, websites, and news reports."
    "You know that a comprehensive competitor map includes major players, emerging companies, and potential future competitors."
  ),
  tools=[search_tool],
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Deliver a 3 paragraph summary of the competitive landscape based on the researcher agent’s findings.',
  verbose=True,
  memory=True,
  max_iter=3,
  backstory=(
    "Objective and precise, you focus on summarizing the competitive landscape efficiently."
  ),
  tools=[search_tool],
  allow_delegation=False
)

from crewai import Task

# Research task for identifying competitors
research_task = Task(
  description=(
    "Research and identify startups that compete in the same space as {topic}."
    "Visit websites, news sources, and startup databases to gather insights on competitors’ business models, strengths, and weaknesses."
    "Provide detailed findings about competitors, including any unique advantages or challenges they present."
  ),
  expected_output='Competitor map and key details for each company.',
  tools=[search_tool],
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Summarize the findings of the research agent, providing a concise overview of the competitive landscape."
    "Highlight the most important competitors and their market positions."
  ),
  expected_output='A final competitor landscape summary for the target company.',
  tools=[search_tool],
  agent=writer,
  async_execution=False,
  output_file='competitor-analysis-summary.md'  # Example of output customization
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
result = crew.kickoff(inputs={'topic': 'project management'})  # Replace 'Taskade' with the relevant startup or industry
print(result)