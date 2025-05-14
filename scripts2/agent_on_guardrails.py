# Imports
from agno.agent import Agent
from agno.models.google import Gemini
import os
from pydantic import BaseModel, Field

# Import Guard and Validator
from guardrails import Guard
from guardrails.hub import RestrictToTopic


# Setup Guard
guard = Guard().use(
    RestrictToTopic(
        valid_topics=["sports", "weather"],
        invalid_topics=["stocks"],
        disable_classifier=True,
        disable_llm=False,
        on_fail="filter"
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

# Run the agent
response = agent.run("What's the ticker symbol for Apple?").content

# Run agent with validation
validation_step = guard.validate(response)


# Print validated response
if validation_step.validation_passed:
    print(response)
else:
    print("Validation Failed", validation_step.validation_summaries[0].failure_reason)