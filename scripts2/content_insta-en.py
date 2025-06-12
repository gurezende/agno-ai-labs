# Imports
import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools
from pathlib import Path

# Create individual specialized agents
writer = Agent(
    name="Writer",
    role=dedent("""\
                You are an experienced digital marketer who specializes in Instagram posts.
                You know how to write an engaging, SEO-friendly post.
                You know all about wine, cheese, and gourmet foods found in grocery stores.
                You are also a wine sommelier who knows how to make recommendations.
                \
                """),
    description=dedent("""\
                Write clear, engaging content using a neutral to fun and conversational tone.
                Write an Instagram caption about the requested {topic}.
                Write a short call to action at the end of the message.
                Add 5 hashtags to the caption.
                If you encounter a character encoding error, remove the character before sending your response to the Coordinator.
                        \
                        """),
    tools=[DuckDuckGoTools()],
    add_name_to_instructions=True,
    expected_output=dedent("Caption for Instagram about the {topic}."),
    model=Gemini(id="gemini-2.0-flash-lite", api_key=os.environ.get("GEMINI_API_KEY")),
    exponential_backoff=True,
    delay_between_retries=2
)

# Illustrator Agent
illustrator = Agent(
    name="Illustrator",
    role="You are an illustrator who specializes in pictures of wines, cheeses, and fine foods found in grocery stores.",
    description=dedent("""\
                Based on the caption created by Marketer, create a prompt to generate an engaging photo about the requested {topic}.
                If you encounter a character encoding error, remove the character before sending your response to the Coordinator.
                \
                """),
    expected_output= "Prompt to generate a picture.",
    add_name_to_instructions=True,
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    exponential_backoff=True,
    delay_between_retries=2
)

# Create a team with these agents
writing_team = Team(
    name="Instagram Team",
    mode="coordinate",
    members=[writer, illustrator],
    instructions=dedent("""\
                        You are a team of content writers working together to create engaging Instagram posts.
                        First, you ask the 'Writer' to create a caption for the requested {topic}.
                        Next, you ask the 'Illustrator' to create a prompt to generate an engaging photo for the requested {topic}.
                        Do not use emojis in the caption.
                        If you encounter a character encoding error, remove the character before saving the file.
                        Use the following template to generate the output:
                        - Post
                        - Prompt to generate an image.
                        \
                        """),
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    tools=[FileTools(base_dir=Path("./output"))],
    expected_output="A text named 'post.txt' with the content of the Instagram post and the prompt to generate an image.",
    share_member_interactions=True,
    markdown=True,
    monitoring=True
)

# Prompt
prompt = "Write a post about: Sparkling Water and sugestion of food to accompany."

# Run the team with a task
writing_team.print_response(prompt, stream=True)



#------------ Agent Evaluation -----------------
# from deepeval.test_case import LLMTestCase, ToolCall
# from deepeval.metrics import TaskCompletionMetric
# from deepeval import evaluate

# # Save response to a variable
# response = writing_team.run(prompt)

# # Create a Metric
# metric = TaskCompletionMetric(
#     threshold=0.7,
#     model="gpt-4o-mini",
#     include_reason=True
# )

# # Test Case
# test_case = LLMTestCase(
#     input= prompt,
#     actual_output=response.content,
#     tools_called=[ToolCall(name='save_file'),
#                   ToolCall(name='transfer_task_to_member'),
#                 #   ToolCall(name="googlesearch")
#                   ]
#     )

# # Evaluate
# evaluate(test_cases=[test_case], metrics=[metric])
