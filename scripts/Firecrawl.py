# Imports
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.firecrawl import FirecrawlTools
import os


# Create agent
agent = Agent(
    model= Gemini(id="gemini-2.0-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
    description= "You are an assistant.",
    tools= [FirecrawlTools(scrape=True)],
    show_tool_calls= True,
    markdown= True
    )

# Run agent
agent.print_response("Summarize: 'https://www.wired.com/story/openai-adds-shopping-to-chatgpt/'", markdown=True)

