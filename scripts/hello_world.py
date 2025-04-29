# Imports
from agno.agent import Agent
from agno.models.google import Gemini
import os

# Create agent
agent = Agent(
    model= Gemini(id="gemini-1.5-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
    description= "An assistant agent",
    instructions= ["Be sucint. Answer in a maximum of 2 sentences."],
    markdown= True
    )

# Run agent
response = agent.run("What's the weather like in NYC in May?")

# Print response
print(response.content)


