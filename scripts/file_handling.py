# Imports
import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.file import FileTools

# Create agent
agent = Agent(
    model= Gemini(id="gemini-1.5-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
                  description= "You are an assistant.",
                  tools=[FileTools(
                      read_files=True, 
                      save_files=True
                      )],
                  show_tool_calls=True)


# Writing and saving a file
agent.print_response("Write a 300 word summary about price optimization with Python and save it to a file named 'price_optimization.md'.",
                     markdown=True)

# Reading a file
agent.print_response("Read the file 'pyproject.toml' and tell me the content in the 'dependencies' section.",
                     markdown=True)