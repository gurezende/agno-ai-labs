# Imports
import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools


# Topic
topic = "Healthy Eating"

# Create agent
agent = Agent(
    model= Gemini(id="gemini-1.5-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
                  description= f"""You are a social media marketer specialized in creating engaging content.
                  Search the internet for 'trending topics about {topic}' and use them to create a post.""",
                  tools=[FileTools(save_files=True),
                         GoogleSearchTools()],
                  expected_output="""A short post for instagram and a prompt for a picture related to the content of the post.
                  Don't use emojis or special characters in the post. If you find an error in the character encoding, remove the character before saving the file.
                  Use the template:
                  - Post
                  - Prompt for the picture
                  Save the post to a file named 'post.txt'.""",
                  show_tool_calls=True,
                  monitoring=True)

# Writing and saving a file
agent.print_response("""Write a short post for instagram with tips and tricks that positions me as 
                     an authority in {topic}.""",
                     markdown=True)