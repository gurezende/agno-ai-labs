# Imports
from agno.agent import Agent
from agno.models.google import Gemini
import os
# Import Guard and Validator
from guardrails.hub import RestrictToTopic
from guardrails import Guard

# Setup Guard
guard = Guard().use(
    RestrictToTopic(
        valid_topics=["sports", "weather"],
        invalid_topics=["stocks"],
        disable_classifier=True,
        disable_llm=False,
        on_fail="exception"
    )
)

# Create agent
agent = Agent(
    model= Gemini(id="gemini-1.5-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
    description= "An assistant agent",
    instructions= ["Be sucint. Reply in maximum two sentences"],
    markdown= True
    )

# Run agent
response = agent.run("What's the ticker symbol for Apple?")
# guard.validate(response.content)

# Print response
print(response.content)
