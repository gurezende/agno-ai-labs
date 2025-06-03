# Imports
from agno.agent import Agent
from agno.models.google import Gemini
import os

# Create agent
agent = Agent(
    model= Gemini(id="gemini-1.5-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
    description= "An assistant agent",
    instructions= ["Be sucint. Return a markdown table"],
    expected_output= "A table with month, season and average temperature",	
    markdown= True,
    monitoring= True
    )

# Run agent
response = agent.print_response("What's the weather like in NYC for each month of the year?",
                                markdown=True)


