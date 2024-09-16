import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# API Keys Setup (you may want to set this securely via streamlit secrets)
os.environ["SERPER_API_KEY"] = "1870ff3ce26db44853ad7478e8ee18293080661c"  # Replace with your serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-9Bvz0fdqJO8C6yX7O6nfT3BlbkFJVuHTEZZodE9zTeqzCRIO"  # Replace with your OpenAI API key

# Initialize the search tool
search_tool = SerperDevTool()

# Streamlit UI
st.title('Competitor Mapping Agent')

# Input field for the startup/industry to analyze
topic = st.text_input('Enter Startup or Industry for Competitor Mapping')

# Button to start the process
if st.button('Run Competitor Mapping Agent') and topic:

    # Competitor Mapping Researcher Agent
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

    # Writer Agent
    writer = Agent(
        role='Writer',
        goal='Deliver a one-paragraph summary of the competitive landscape based on the researcher agent’s findings, including insights into key competitors.',
        verbose=True,
        memory=True,
        max_iter=3,
        backstory=(
            "Objective and precise, you focus on summarizing the competitive landscape efficiently."
            "You are comfortable highlighting key players and identifying competitive advantages and risks."
        ),
        tools=[search_tool],
        allow_delegation=False
    )

    # Define the research task
    research_task = Task(
        description=(
            "Research and identify startups and established companies that compete in the same space as {topic}."
            "Visit websites, news sources, and startup databases to gather insights on competitors’ business models, strengths, and weaknesses."
            "Provide detailed findings about competitors, including any unique advantages or challenges they present."
        ),
        expected_output='Competitor map and key details for each company.',
        tools=[search_tool],
        agent=researcher,
    )

    # Define the writing task
    write_task = Task(
        description=(
            "Summarize the findings of the research agent, providing a concise overview of the competitive landscape."
            "Highlight the most important competitors and their market positions."
        ),
        expected_output='A final competitor landscape summary for the target company.',
        tools=[search_tool],
        agent=writer,
        async_execution=False,
        output_file='competitor-analysis-summary.md'  # Output file to save the summary (optional)
    )

    # Create the crew and process
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,  # Tasks run in sequence
        memory=True,
        cache=True,
        max_rpm=100,
        share_crew=True
    )

    # Execute the process
    with st.spinner('Mapping competitors, please wait...'):
        result = crew.kickoff(inputs={'topic': topic})

    # Display results
    st.success('Competitor mapping completed!')
    st.write(result)

else:
    st.info("Please enter a startup or industry to start the process.")
