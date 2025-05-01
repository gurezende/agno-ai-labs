# Imports
import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder



# Load webpage to the knowledge base
agent_knowledge = UrlKnowledge(
    urls=["https://gustavorsantos.me/?page_id=47"],
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="projects",
        search_type=SearchType.hybrid,
        # Use Sentence Transformer for embeddings
        embedder=SentenceTransformerEmbedder(),
    ),
)

# Create agent
agent = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    instructions=[
        "Use tables to display data.",
        "Search your knowledge before answering the question.",
        "Only inlcude the content from the agent_knowledge base table 'projects'",
        "Only include the output in your response. No other text.",
    ],
    knowledge=agent_knowledge,
    add_datetime_to_instructions=True,
    markdown=True,
)

if __name__ == "__main__":
    # Load the knowledge base, comment out after first run
    # Set recreate to True to recreate the knowledge base if needed
    agent.knowledge.load(recreate=False)
    agent.print_response(
        "What are the two books listed in the 'agent_knowledge'",
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
    )