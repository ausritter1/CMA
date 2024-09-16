import os
os.environ["SERPER_API_KEY"] = "1870ff3ce26db44853ad7478e8ee18293080661c"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-9Bvz0fdqJO8C6yX7O6nfT3BlbkFJVuHTEZZodE9zTeqzCRIO"

from crewai import Agent
from crewai_tools import SerperDevTool
search_tool = SerperDevTool()

# Creating a researcher agent for finding specific fundraising deal announcements
deal_researcher = Agent(
    role='Fundraising Deal Researcher',
    goal='Find specific links to recent startup fundraising announcements (within the past week).',
    verbose=True,
    memory=True,
    max_iter=10,
    backstory=(
        "Your task is to find articles or announcements that specifically mention startup fundraising deals."
        "Look for phrases like 'raised $X million', 'funding round', 'Series A', 'seed funding', and similar deal-specific language."
        "Exclude general tech news websites, focus only on links directly tied to fundraising announcements from the past week."
    ),
    tools=[search_tool],
    allow_delegation=True
)

# Writer agent for listing specific deal announcement links
deal_writer = Agent(
    role='Writer',
    goal='Provide a list of specific links to recent startup fundraising deal announcements based on the researcher’s findings.',
    verbose=True,
    memory=True,
    max_iter=3,
    backstory=(
        "You summarize and list links directly tied to specific startup fundraising deals."
    ),
    tools=[search_tool],
    allow_delegation=False
)

from crewai import Task

# Research task for finding recent fundraising deal announcements
deal_research_task = Task(
    description=(
        "Research and find startup fundraising announcements from the past week."
        "Only return links to articles or press releases that specifically mention the fundraising event for each startup."
        "Use phrases like 'raised $X million', 'Series A', 'seed round', and similar funding-specific terms."
        "Avoid general tech news websites and homepages. Focus only on direct announcements or press releases."
    ),
    expected_output='List of article links to startup fundraising deals announced in the past week.',
    tools=[search_tool],
    agent=deal_researcher,
)

# Writing task for compiling the list of fundraising article links
deal_write_task = Task(
    description=(
        "Summarize the researcher agent’s findings by providing a concise list of links directly to startup fundraising deal announcements from the past week."
    ),
    expected_output='A final list of article links directly related to startup fundraising deals.',
    tools=[search_tool],
    agent=deal_writer,
    async_execution=False,
    output_file='recent-fundraising-deals.md'  # Customize the output
)

from crewai import Crew, Process

# Forming the crew for fundraising deal news search
fundraising_deal_crew = Crew(
    agents=[deal_researcher, deal_writer],
    tasks=[deal_research_task, deal_write_task],
    process=Process.sequential,  # Optional: Sequential task execution is default
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Starting the task execution process with feedback
result = fundraising_deal_crew.kickoff(inputs={'topic': 'recent startup fundraising announcements'})
print(result)