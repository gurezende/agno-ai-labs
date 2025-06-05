from agno.agent import Agent
from agno.models.google import Gemini
import os
from agno.tools.yfinance import YFinanceTools
from agno.tools.file import FileTools

# Web-Search Agent 
agent = Agent(model= Gemini(id="gemini-2.0-flash",
              api_key = os.environ.get("GEMINI_API_KEY")),
              tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True),
                     FileTools(read_files=True, save_files=True)],
              description= "You are a seasoned investment analyst. You can use FileTools to read and save files.",
              instructions= ["Get the data from the requested stock",
                             "Analyze the data and provide insights",
                             "Use FileTools to read and save files"],
              expected_output="Format your response using markdown and use tables to display data where possible. Save results to a file named 'results.md'."
              )

# Run agent
agent.print_response(
    f"Share the NVDA stock price and analyst recommendations",
    markdown=True
    )