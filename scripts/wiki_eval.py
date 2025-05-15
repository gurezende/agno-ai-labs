# Imports
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.wikipedia import WikipediaTools
import os

# Prompt
prompt = "Search wikipedia for 'Time series analysis' and summarize the 3 main points"

# Create agent
agent = Agent(
    model= Gemini(id="gemini-2.0-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
    description= "You are a researcher specialized in searching the wikipedia.",
    tools= [WikipediaTools()],
    show_tool_calls= True,
    markdown= True,
    read_tool_call_history= True
    )

# Run agent
response = agent.run(prompt)


# Print response
print(response.content)

#------------ Evaluation -----------------
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import TaskCompletionMetric
from deepeval import evaluate

# Create a Metric
metric = TaskCompletionMetric(
    threshold=0.7,
    model="gpt-4o-mini",
    include_reason=True
)

# Test Case
test_case = LLMTestCase(
    input=prompt,
    actual_output=response.content,
    tools_called=[ToolCall(name="wikipedia")]
    )

# Evaluate
evaluate(test_cases=[test_case], metrics=[metric])

