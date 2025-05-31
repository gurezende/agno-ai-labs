# Imports
import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools


# ------------------------- Define the Topic --------------------------------
topic = "A step-by-step guide to make your first $1000 of passive income with AI"
# ---------------------------------------------------------------------------


# Create individual specialized agents

# Researcher Agent: look for content related to the topic and create an outline
researcher = Agent(
    name="Researcher",
    role=dedent(f"""\
                You are an experienced researcher specialized in making money online.
                You know about affiliate marketing, paid advertising, content marketing, SEO, and more.
                You are also an expert in researching the latest trends in the solopreneurship industry.
                Research about {topic} and use the content you find in the Internet to make an outline of an article.
                \
                """),
    expected_output="An outline of the article to be passed to the 'Writer'.",
    tools=[GoogleSearchTools()],
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    add_name_to_instructions=True,
    exponential_backoff=True,
    delay_between_retries=2
)

# Writer Agent: write the article
writer = Agent(
    name="Writer",
    role=dedent(f"""\
                You are an experienced content writer specialized in making money online, solopreneurship, passive income.
                Using the outline you received from the 'Researcher', write a blog post article about: {topic}.
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
                3. Include 2 relevant ideas of AI prompts to make money with {topic}.
                4. Include the links, references, and sources.
                Save the article to a file named 'article.md'.
                If you saved the article, end the job and send it to the 'Editor'.            
                \
                """),
    tools=[FileTools(read_files=True, save_files=True)],
    expected_output=dedent("""\
                           A blog post article in markdown format with approximately 700 words with the following structure:
                           - Title
                           - Intro
                           - Body
                           - AI Prompts
                           - Conclusion
                           - References
                           \
                           """),
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    add_name_to_instructions=True,
    exponential_backoff=True,
    delay_between_retries=10
)

# Editor Agent: proofread the article
editor = Agent(
    name="Editor",
    role=dedent("""\
                You are an experienced Editor specialized in fact checking the content.
                Once you receive the article from the 'Writer', check it for grammar, punctuation, and spelling errors.
                If you find any, correct them.
                Make sure to use the style of the writer.
                Fact check the links and sources. 2 times is enough.
                Keep track of how many checks you did, so you don't fall into a loop of checking.
                Once you can't find any errors, save the revised article to a file named 'article.md' and end the job.
                If you saved the article, end the job.
                \
                """),
    expected_output= "A revised blog post article in markdown format saved to a file named 'article.md'.",
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    add_name_to_instructions=True,
    exponential_backoff=True,
    delay_between_retries=5
)

# Illustrator Agent: create a cover image
illustrator = Agent(
    name="Illustrator",
    role=dedent("""\
                You are an illustrator who specializes in illustrating blog posts.
                Based on the 'article.md' created by the 'Writer', create a prompt to generate an engaging photo about the requested {topic}.
                Save the prompt to a file named 'prompt.txt'.
                \
                """),
    tools=[FileTools(read_files=True, save_files=True)],
    expected_output= "Text file with Prompt for AI to generate a picture",
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    add_name_to_instructions=True,
    exponential_backoff=True,
    delay_between_retries=5
)

# Create a team with these agents
writing_team = Team(
    name="Writing Team",
    mode="coordinate",
    members=[researcher, writer, editor, illustrator],
    instructions=dedent(f"""\
                        You are a team of content writers that work together to create high-quality blog posts.
                        First ask the Researcher to search for the most relevant URLs for the {topic} and create the article outline.
                        Then ask the Writer to get an engaging draft of the article.
                        Send the article to the Editor to for editing, proofread, and refineing.
                        Once the article is ready, ask the Illustrator to create a prompt for AI to generate a picture.
                        Remember: you are the final gatekeeper before the article is published, so make sure the article is great.
                        Don't allow more than 2 edits/ saves.
                        \
                        """),
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    expected_output="A blog post article with approximately 700 words about {topic} saved to a file named 'article.md' and a prompt for AI to generate a picture saved to a file named 'prompt.txt'.",
    markdown=True,
    monitoring=True,
    enable_agentic_context=True,
    show_tool_calls=True
)

# Run the team with a task
writing_team.print_response("Create an article about: {topic} .")