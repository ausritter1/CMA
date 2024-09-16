import os
import streamlit as st
import time

# Set environment variables for API keys
os.environ["SERPER_API_KEY"] = "1870ff3ce26db44853ad7478e8ee18293080661c"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-9Bvz0fdqJO8C6yX7O6nfT3BlbkFJVuHTEZZodE9zTeqzCRIO"

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

# Define the researcher agent
researcher = Agent(
    role='Senior Researcher',
    goal='Find hyperaccurate real world data to build precise market sizing models',
    verbose=True,
    memory=True,
    max_iter=6,
    backstory=(
        "Driven by the commitment to getting as close an estimate as possible of the true market size for a startup."
        "You understand that despite the challenges and uncertainties, you must come up with an estimated final, single answer for TAM."
    ),
    tools=[search_tool],
    allow_delegation=True
)

# Define the writer agent
writer = Agent(
    role='Writer',
    goal='Deliver precise and substantiated analyses of the TAM (Total Addressable Market) for the provided startup.',
    verbose=True,
    memory=True,
    max_iter=2,
    backstory=(
        "Devoid of emotion, only interested in delivering the most accurate report possible."
        "Able to guess and make calculated predictions when necessary to save time."
    ),
    tools=[search_tool],
    allow_delegation=False
)

# Define the research task
research_task = Task(
    description=(
        "You will calculate TAM in USD by multiplying the max number of potential users of the startup by the price of the product."
        "Learn information about the startup, {topic}. Visit their website and ensure you find information related to product pricing."
        "Your final report should include everything the writer agent needs to deliver an accurate assessment of the startup's TAM."
    ),
    expected_output='Estimate for TAM',
    tools=[search_tool],
    agent=researcher,
)

# Define the writing task
write_task = Task(
    description=(
        "Briefly organize the information compiled by the research agent."
        "Provide a final TAM estimate for the startup in $USD"
    ),
    expected_output='A final market sizing report.',
    tools=[search_tool],
    agent=writer,
    async_execution=False,
    output_file='new-blog-post.md'  # Example of output customization
)

# Define the crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Optional: Sequential task execution is default
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Streamlit app setup
st.set_page_config(page_title="Market Sizing Analysis", layout="wide")

st.title("Startup Market Sizing Analysis")
st.write("Enter the name of a startup to get a market sizing analysis performed by our intelligent agents.")

# User input
startup_name = st.text_input("Startup Name:", "")

# Define placeholders for displaying progress and results
placeholder = st.empty()
result_placeholder = st.empty()

if st.button("Analyze"):
    if startup_name:
        with placeholder.container():
            st.write(f"Analyzing market size for startup: **{startup_name}**")
            progress_text = st.empty()

        # Kickoff the crew process
        inputs = {'topic': startup_name}
        result = crew.kickoff(inputs=inputs)

        # Simulate progress updates
        for i in range(6):
            progress_text.text(f"Researcher agent is working... Step {i+1}/6")
            time.sleep(2)

        progress_text.text("Writer agent is compiling the final report...")

        # Display final results
        result_placeholder.markdown(f"### Market Sizing Analysis for {startup_name}")
        result_placeholder.write(result)
    else:
        st.warning("Please enter a startup name to analyze.")

# Style improvements
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
    }
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)