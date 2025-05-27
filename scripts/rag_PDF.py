# Imports
import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.qdrant import Qdrant
from pathlib import Path


# Collection name for QDrand
COLLECTION_NAME = "pdf-reader"

# Instance of Qdrant (Vector DB)
vector_db = Qdrant(collection=COLLECTION_NAME, location=":memory:")


# Create PDF the knowledge base
pdf_knowledge_base = PDFKnowledgeBase(
    path= Path("C:/Users/gurez/OneDrive/Área de Trabalho/attention-is-all-you-need-Paper.pdf"),
    vector_db= vector_db,
    reader=PDFReader(chunk=True)
)

# Create agent
agent = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    instructions=[
        "Search your knowledge before answering the question.",
        "Only include the content from the agent_knowledge base table 'pdf_documents'",
        "Only include the output in your response. No other text.",
    ],
    knowledge=pdf_knowledge_base,
    search_knowledge=True,
    markdown=True,
)

# Test
if __name__ == "__main__":
    
    # Prompt
    prompt = "What is attention? Explain in simple terms"

    # Load the knowledge base, comment out after first run
    # Set recreate to True to recreate the knowledge base if needed
    agent.knowledge.load(recreate=False)

    # Run agent
    agent.print_response(
        prompt,
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True
    )