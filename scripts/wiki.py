# Imports
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.wikipedia import WikipediaTools
import os


# Create agent
agent = Agent(
    model= Gemini(id="gemini-2.0-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
    description= "You are a researcher specialized in searching the wikipedia.",
    tools= [WikipediaTools()],
    show_tool_calls= True,
    markdown= True
    )

# Run agent
agent.print_response("Search wikipedia for 'Time series analysis' and summarize the 3 main points", markdown=True)