# Imports
import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools

# Create individual specialized agents
researcher = Agent(
    name="Researcher",
    role=dedent("""\
                You are an experienced researcher specialized in making money online.
                You know about affiliate marketing, paid advertising, content marketing, SEO, and more.
                You are also an expert in researching the latest trends in the solopreneurship industry.
                Research about {topic} and use the content you find in the Internet to make an outline of an article.
                \
                """),
    expected_output="An outline of the article.",
    tools=[GoogleSearchTools()],
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY"))
)

writer = Agent(
    name="Writer",
    role=dedent("""\
                You are an experienced content writer specialized in making money online, solopreneurship, passive income.
                Using the outline you received from the 'Researcher', write a blog post article about: {topic}.
                Write a clear, and engaging content, using a neutral to fun tone. Don't exagerate.
                Include the links, references, and sources.
                Save the article to a file named 'article.md'.              
                \
                """),
    expected_output=dedent("""\
                           A blog post article in markdown format with approximately 700 words with the following structure:
                           - Title
                           - Intro
                           - Body
                           - Conclusion
                           - References
                           \
                           """),
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY"))
)

editor = Agent(
    name="Editor",
    role=dedent("""\
                You are an experienced Editor specialized in fact checking the content.
                Once you receive the article from the 'Writer', check it for grammar, punctuation, and spelling errors.
                If you find any, correct them.
                Make sure to use the style of the writer.
                Fact check the links and sources.
                Perform a maximum of 2 rounds of checking, save the revised article to a file named 'article.md' and end the job.   
                \
                """),
    expected_output= "A revised blog post article in markdown format saved to a file named 'article.md'.",
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY"))
)

# Create a team with these agents
writing_team = Team(
    name="Writing Team",
    mode="coordinate",
    members=[researcher, writer, editor],
    instructions="You are a team of content writers that work together to create high-quality blog posts about {topic}.",
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    tools=[FileTools(read_files=True, save_files=True)],
    expected_output="A blog post article with approximately 700 words about {topic} saved to a file named 'article.md'.",
    markdown=True,
)

# Run the team with a task
writing_team.print_response("Create an article about the topic: 'Here is how to Write a Proposal to Be Noticed in Upwork'")