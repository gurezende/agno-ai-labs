from textwrap import dedent
import os
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.tools.file import FileTools
from pathlib import Path

def get_job_description_file():
    """
    Reads the job description from a file named 'job_description.md' in the jobs folder.

    Returns:
        str: The content of the job description file.
    """
    job_description_file = Path("./jobs/job_description.md").read_text()
    return job_description_file


def get_resume_file():
    """
    Reads the resume from a file named 'resume.md' in the jobs folder.

    Returns:
        str: The content of the resume file.
    """
    resume_file = Path("./jobs/resume.md").read_text()
    return resume_file


# Profiler Agent
profiler_agent = Agent(
    name="Profiler",
    model=OpenAIChat(id="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY")),
    # model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    description=dedent("""\
        You are an experienced HR professional that is expert analyzing job descriptions and understanding the job requirements.
        You create profiles that highlight the job requirements and align them with the candidate's skills and experience.
        \
    """),
    instructions=dedent("""\
        Use your context to get the 'job description'.
        Analyze the job description to extract the most important requirements and ATS keywords.
        Write a profile that highlights which skills and experiences match the job requirements.
        Highlight ATS keywords for the writer to create an ATS optimized resume.
    \
    """),
    context={'job_description':	get_job_description_file},
    add_context=True,
    expected_output=dedent("""A structured list of job requirements, including necessary skills, 
                              qualifications, and experiences and how they align with the 
                              candidate's skills and experience."""),
    add_name_to_instructions=True,
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True)

# Writer Agent
writer_agent = Agent(
    name="Writer",
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    # model=OpenAIChat(id="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY")),

    description=dedent("""\
        You are an experienced HR professional that is expert in writing compelling resumes for job interviews.
        You know how to write a resume that highlights your skills and experience, and how to explain your qualifications to potential employers.
        \
    """),
    instructions=dedent("""\
        Analyze the output from the 'Profiler'.
        Use your context to read the candidate's 'resume' to match the most important requirements to the job requirements.
        Leverage and rephrase the candidate's experiences to align with the job requirements and ATS keywords. 
        Use relevant experiences and projects from the candidate's GitHub profile 'https://github.com/gurezende'.
        Do not make up information about the candidate experience or projects.
        Do not add skills that the candidate does not have.
        Keep the resume structure, and enhance the content to align with the job requirements.
        Write an ATS optimized resume that highlights your skills and experience, and explains your qualifications to potential employers.
    \
    """),
    context={'resume':get_resume_file},
    add_context=True,
    add_name_to_instructions=True,
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
                        First, you ask the 'Profiler' to analyze the job description from its context and to extract the most important requirements and ATS keywords.
                        Next, you ask the 'Writer' to write an ATS optimized resume that highlights your skills and experience, and explains your qualifications to potential employers.
                        Save the resume to a file named 'tailored_resume.md'.
                        \
                        """),
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    # model=OpenAIChat(id="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY")),
    tools=[FileTools(base_dir=Path("./jobs"), read_files=True, save_files=True)],
    share_member_interactions=True,
    show_members_responses=True,
    # enable_agentic_context=True,
    expected_output="A tailored resume that fits perfectly with the job requirements, saved to a file named 'tailored_resume.md'.",
    markdown=True,
    monitoring=True
)

# Prompt
prompt = "Create a tailored and ATS optimized version of 'resume' that fits perfectly with the job requirements for 'job_description'."

# Run the team with a task
resume_team.print_response(prompt, stream=True)

