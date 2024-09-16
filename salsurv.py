import os
os.environ["SERPER_API_KEY"] = "1870ff3ce26db44853ad7478e8ee18293080661c"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-9Bvz0fdqJO8C6yX7O6nfT3BlbkFJVuHTEZZodE9zTeqzCRIO"

from crewai import Agent
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Senior Researcher',
  goal='search the web based on an email input, {topic}, and find the target persons job title via linkedin. it will be the first search result.',
  verbose=True,
  memory=True,
  max_iter=5,
  backstory=(
    "You can search the web and find linkedin profiles and extract job titles."
  ),
  tools=[search_tool],
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Write the most likely job title for the person based on the research agent search results',
  verbose=True,
  memory=True,
  max_iter=2,
  backstory=(
    "Expert writer"
  ),
  tools=[search_tool],
  allow_delegation=False
)

from crewai import Task

# Research task
research_task = Task(
  description=(
    "The task is to take the email input of a person, {topic}, and search the web to try to find their job title via linkedin search results. Then return the most likely job title for that person which should be the first search result. No need to search beyond that.."
  ),
  expected_output='job title from top search result',
  tools=[search_tool],
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Write the most likely job title for the person based on the research agents search results."
  ),
  expected_output='job title from top search result.',
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
result = crew.kickoff(inputs={'topic': 'sridhar@vmgpartners.com'})
print(result)