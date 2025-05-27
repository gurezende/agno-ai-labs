from textwrap import dedent
import os
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.tools.github import GithubTools
from agno.tools.file import FileTools
from pathlib import Path



# Profiler Agent
profiler_agent = Agent(
    name="Profiler",
    model=OpenAIChat(id="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY")),
    # model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    tools=[FileTools(base_dir=Path("jobs"), read_files=True)],
    description=dedent("""\
        You are an experienced HR professional that is expert analyzing job descriptions and understanding the job requirements.
        You create profiles that highlight the job requirements and align them with the candidate's skills and experience.
        \
    """),
    instructions=dedent("""\
        Use your tools to open the job description file ('job_description.md').
        Analyze the job description to extract the most important requirements and ATS keywords.
        Write a profile that highlights which skills and experiences match the job requirements.
        Highlight ATS keywords for the writer to create an ATS optimized resume.
    \
    """),
    expected_output=dedent("A structured list of job requirements, including necessary skills, qualifications, and experiences and how they align with the candidate's skills and experience."),
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True)

# Writer Agent
writer_agent = Agent(
    name="Writer",
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    # model=OpenAIChat(id="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY")),
    tools=[FileTools(base_dir=Path("jobs"), read_files=True, save_files=True),
           GithubTools(base_url="https://github.com/gurezende", search_repositories=True, access_token=os.environ.get("GITHUB_ACCESS_TOKEN"))],
    description=dedent("""\
        You are an experienced HR professional that is expert in writing compelling resumes for job interviews.
        You know how to write a resume that highlights your skills and experience, and how to explain your qualifications to potential employers.
        \
    """),
    instructions=dedent("""\
        Analyze the output from the 'Profiler'.
        Use your tools to read the candidate's resume file ('resume.md') to match the most important requirements to the job requirements.
        Use relevant experiences and projects from the candidate's GitHub profile 'https://github.com/gurezende'.
        Do not make up information about the candidate experience or projects.
        Keep the resume structure, and enhance the content to align with the job requirements.
        Write an ATS optimized resume that highlights your skills and experience, and explains your qualifications to potential employers.
    \
    """),
    expected_output=dedent("An ATS optimized resume that fits perfectly with the job requirements."),
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
)

# Create a team with these agents
resume_team = Team(
    name="Resume Team",
    mode="coordinate",
    members=[profiler_agent, writer_agent],
    instructions=dedent("""\
                        You are a team of experts that are expert in writing compelling resumes for job interviews.
                        First, you ask the 'Profiler' to analyze the job posting and to extract the most important requirements and ATS keywords.
                        Next, you ask the 'Writer' to write an ATS optimized resume that highlights your skills and experience, and explains your qualifications to potential employers.
                        Save the resume to a file named 'tailored_resume.md'.
                        \
                        """),
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    # model=OpenAIChat(id="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY")),
    expected_output="A tailored resume that fits perfectly with the job requirements, saved to a file named 'tailored_resume.md'.",
    markdown=True,
    monitoring=True
)

# Prompt
prompt = "Create a tailored version of 'resume.md' that fits perfectly with the job requirements for 'job_description.md'."

# Run the team with a task
resume_team.print_response(prompt)

