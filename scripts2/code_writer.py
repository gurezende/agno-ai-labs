# Imports
import os
from dotenv import load_dotenv
from pathlib import Path
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini

from agno.team import Team
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools
load_dotenv()

# ------------------------- Define the Topic --------------------------------
topic = "Top 7 SQL tricks for Data Scientists"
model = 'gemini-2.0-flash' #"gemini-2.5-pro-exp-03-25"
# ---------------------------------------------------------------------------


# Create individual specialized agents

# Researcher Agent: look for content related to the topic and create an outline
researcher = Agent(
    name="Researcher",
    role=dedent(f"""\
                You are an experienced researcher specialized in Data Science and Techonology.
                You are expert about coding, AI, and machine learning.
                You are also an expert in researching solutions to business problems using programming languages Python, R and SQL.
                \
                """),
    description=dedent(f"""\
                Research about {topic} and use the content you find in the Internet to make an outline of an article.
                Do not write code. This is a task for the 'Coder' agent.
                This outline must have the blog post structure and an idea of problem to be solved via code by the 'Coder' agent.
                \
                """),
    expected_output="An outline of the article to be passed to the 'Writer'.",
    tools=[GoogleSearchTools()],
    model=Gemini(id=model, api_key=os.environ.get("GEMINI_API_KEY")),
    add_name_to_instructions=True,
    exponential_backoff=True,
    delay_between_retries=5
)

# Researcher Agent: look for content related to the topic and create an outline
coder = Agent(
    name="Coder",
    role=dedent(f"""\
                You are an experienced developer specialized in Python, SQL and R.
                You are expert about creating small, clear, and efficient code.
                \
                """),
    description=dedent(f"""\
                Write a code solution to the problem stated in the outline you received from the 'Researcher' agent.
                Your entire script is well commented and should be small, with less than 100 lines, if possible.
                Check the content received from the 'Researcher' and use the problem stated in the content to create the script solution.
                Use the best language for the topic, knowing that your order of preference is Python, SQL, and R.
                \
                """),
    expected_output="A script to be passed to the 'Writer'.",
    add_name_to_instructions=True,
    tools=[GoogleSearchTools()],
    model=Gemini(id=model, api_key=os.environ.get("GEMINI_API_KEY")),
    exponential_backoff=True,
    delay_between_retries=5
)

# Writer Agent: write the article
writer = Agent(
    name="Writer",
    role="You are an experienced content writer specialized in Data Science, AI, Techonology, and Business.",
    description=dedent(f"""\
                Using the outline you received from the 'Researcher', and the script you received from the 'Coder', write a blog post article about: {topic}.
                Writing guidelines:
                1. Tone and voice
                 - Use a conversational, friendly tone.
                 - Don't exagerate.
                 - Address reader directly as 'you' or 'your'. 
                 - Incorporate contractions and coloquialism.
                 - Balance professionalism and approachability.
                 - Not more than 35-40 words per paragraph.
                 - Avoid old fancy adjectives.
                 - Write a clear, and engaging content.
                2. Engagement techniques
                 - Ask rethorical questions to involve the reader.
                 - Use occasional humor.
                 - Anticipate and address potential reader's questions.
                 - Use real life examples.
                3. Explain the code you received from the 'Coder' agent and give examples of real life applications.
                4. Include the links, references, and sources of coding documentation.
                Once done, save the article to a file named 'coding_article.md' and send the article to the 'Editor'.
                \
                """),
    add_name_to_instructions=True,
    tools=[FileTools(read_files=True, save_files=True, base_dir=Path("./articles"))],
    expected_output=dedent("""\
                           A blog post article in markdown format with approximately 700 words with the following structure:
                           - Title
                           - Intro
                           - Body
                            - Code Walk-Trough
                           - Conclusion
                           - References
                           \
                           """),
    model=Gemini(id=model, api_key=os.environ.get("GEMINI_API_KEY")),
    exponential_backoff=True,
    delay_between_retries=10
)

# Editor Agent: proofread the article
editor = Agent(
    name="Editor",
    role="You are an experienced Coding Editor specialized in checking the content",
    description=dedent("""\
                Once you receive the article from the 'Writer', check it for grammar, punctuation, and spelling errors.
                If you find any, correct them.
                Make sure to use the style of the writer.
                Check the code you received from the 'Coder' agent for errors.
                Fact check the links and sources. 2 times is enough.
                Keep track of how many checks you did, so you don't fall into a loop of checking.
                Once you can't find any errors, save the revised article to a file named 'coding_article.md' and end the job.
                \
                """),
    expected_output= "A revised blog post article in markdown format saved to a file named 'coding_article.md'.",
    model=Gemini(id=model, api_key=os.environ.get("GEMINI_API_KEY")),
    tools=[FileTools(read_files=True, save_files=True, base_dir=Path("./articles"))],
    add_name_to_instructions=True,
    exponential_backoff=True,
    delay_between_retries=5
)

# Illustrator Agent: create a cover image
illustrator = Agent(
    name="Illustrator",
    role="You are an illustrator specialized in illustrating blog posts",
    description=dedent("""\
                Based on the 'coding_article.md' saved by the 'Editor', create a prompt to generate an engaging photo about the requested {topic}.
                Save the prompt to file.
                \
                """),
    tools=[FileTools(read_files=True, save_files=True, base_dir=Path("./articles"))],
    expected_output= "Text file named 'prompt.txt' with Prompt for AI to generate a picture",
    model=Gemini(id=model, api_key=os.environ.get("GEMINI_API_KEY")),
    add_name_to_instructions=True,
    exponential_backoff=True,
    delay_between_retries=3
)

# Create a team with these agents
writing_team = Team(
    name="Writing Team",
    mode="coordinate",
    members=[researcher, coder, writer, editor, illustrator],
    instructions=dedent(f"""\
                        You are a team of content writers that work together to create high-quality blog posts.
                        First ask the 'Researcher' to search for the most relevant URLs for the {topic} and create the article outline.
                        Send the article outline to the 'Coder' to get the script.
                        Then ask the 'Writer' to get an engaging draft of the article.
                        Send the article to the 'Editor' to for editing, proofread, and refineing.
                        Once the article is ready, ask the 'Illustrator' to create a prompt for AI to generate a picture.
                        Don't allow more than 2 edits/ saves.
                        \
                        """),
    model=Gemini(id=model, api_key=os.environ.get("GEMINI_API_KEY")),
    expected_output="A blog post article with approximately 700 words saved to a file named 'coding_article.md' and a prompt text for AI to generate a picture saved to a file named 'prompt.txt'.",
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    markdown=True,
    monitoring=True
)

# Run the team with a task
writing_team.print_response("Create an article about: {topic}.",
                            stream_intermediate_steps=True)