from agno.agent import Agent
from agno.models.google import Gemini
import os
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.file import FileTools
from pathlib import Path
import dotenv

url = "https://en.wikipedia.org/wiki/List_of_largest_banks"

# Web-Search Agent 
agent = Agent(model= Gemini(id="gemini-1.5-flash",
              api_key = os.environ.get("GEMINI_API_KEY")),
              tools=[FirecrawlTools(scrape=True, formats=["markdown"]),
                     FileTools(read_files=True, save_files=True, base_dir=Path("./output"))],
              description= "You are an assistant that can search the web, read and save files.",
              instructions= ["Use the Firecrawl tool to scrape the website",
                             "Get the result scraped from the url and save it to a file named 'content.md'"
                             "Use FileTools to read and save files",
                             ],
              expected_output="The website's content."
              )

# Run agent
agent.print_response(
    f"Get the Firecrawl result scraped from {url} and save it to a file named 'content.md'",
    markdown=True
   ) 