# Imports
import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.file import FileTools
from openpyxl import load_workbook
from openpyxl.comments import Comment
import pandas as pd


def convert_to_csv(file_path:str):
   """
    Use this tool to convert the excel file to CSV.

    * file_path: Path to the Excel file to be converted
    """
   # Load the file  
   df = pd.read_excel(file_path)

   # Convert to CSV
   return df.to_csv('temp.csv', index=False)
   

# Custom Tool to add comments to the header of an Excel file
def add_comments_to_header(file_path:str, data_dict:dict):
    """
    Use this tool to add the data dictionary as comments to the header of an Excel file.

    The function takes a file path as argument and adds the {data dictionary} as comments to each cell
    Start counting from column 0
    in the first row of the Excel file, using the following format:    
        * Column Number: <column_number>
        * Column Name: <column_name>
        * Data Type: <data_type>
        * Description: <description>
        * Null Values: <number_of_null_values>

    Parameters
    ----------
    * file_path : str
        The path to the Excel file to be processed
    * data_dict : dict
        The data dictionary containing the column number, column name, data type, description, and number of null values

    Returns
    -------
    None
    """

    # Load the workbook
    wb = load_workbook(file_path)

    # Get the active worksheet
    ws = wb.active

    # Iterate over each column in the first row (header)
    for n, col in enumerate(ws.iter_cols(min_row=1, max_row=1)):
        for header_cell in col:
            header_cell.comment = Comment(dedent(f"""\
                              ColName: {data_dict[str(n)]['ColName']}, 
                              DataType: {data_dict[str(n)]['DataType']},
                              Description: {data_dict[str(n)]['Description']},
                              Null Values: {data_dict[str(n)]['Null Values']}\
    """),'AI Agent')

    # Save the workbook
    wb.save('final.xlsx')


# Create the agent
agent = Agent(
    model=Gemini(id="gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY")),
    description= dedent("""\
                        You are an agent that reads the dataset presented to you and 
                        determine the following information:
                        - The data types of each column
                        - The description of each column                   
                        - The number of null values in each column

                        Using the tools provided, create a data dictionary in JSON format that includes the below information:
                        {<ColNumber>: {ColName: <ColName>, DataType: <DataType>, Description: <Description>, Null Values: <number_of_null_values>}}
                        \
                        """),
    tools=[convert_to_csv,
           FileTools(read_files=True),
           add_comments_to_header],
    show_tool_calls=True
    )


# Run the agent
agent.print_response(dedent("""\
                            1. Read the dataset 'data.xlsx' and convert it to a temporary CSV using the 'convert_to_csv' tool.
                            2. Use the temp.csv as input to create the data dictionary for the columns in the dataset. Save the data dictionary to a file named 'data_dict.json'.
                            3. Use the file 'data_dict.json' as input to the tool 'add_comments_to_header'and add the data dictionary as comments to the header of the dataset.
                            \
                            """),
                     markdown=True)

# Remove temporary files
os.remove('temp.csv')
os.remove('data_dict.json')