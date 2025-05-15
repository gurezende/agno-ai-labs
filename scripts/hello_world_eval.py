# Imports
from agno.agent import Agent
from agno.models.google import Gemini
import os
# Evaluation Modules
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval

# Prompt
prompt = "Describe the weather in NYC for May"

# Create agent
agent = Agent(
    model= Gemini(id="gemini-1.5-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
    description= "An assistant agent",
    instructions= ["Be sucint"],
    markdown= True,
    monitoring= True
    )

# Run agent
response = agent.run(prompt)

# Print response
print(response.content)

# Test Case
test_case = LLMTestCase(input=prompt, actual_output=response)

# Setup the Metric
coherence_metric = GEval(
    model='gpt-4o-mini',
    name="Coherence",
    criteria="Coherence. The agent can answer the prompt and the response makes sense.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT]
)

# Run the metric
coherence_metric.measure(test_case)
print(coherence_metric.score)
print(coherence_metric.reason)

# Check the logs
print(coherence_metric.verbose_logs)
