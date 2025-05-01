# Imports
import os
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.reasoning import ReasoningTools


# Create agent with reasoning
agent = Agent(
    model= Groq(id="qwen-qwq-32b",
                  api_key = os.environ.get("GROQ_API_KEY")),
                  description= "You are an experienced math teacher.",
                  tools=[ReasoningTools(add_instructions=True)],
                  show_tool_calls=True)


# Writing and saving a file
agent.print_response("""Explain the concept of sin and cosine in simple terms.""",
                     stream=True,
                     show_full_reasoning=True,
                     markdown=True)
