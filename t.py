# Imports
import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.file import FileTools
from youtube_transcript_api import YouTubeTranscriptApi

# Get YT transcript
def get_yt_transcript(video_id:str) -> str:
      
    """
    Use this function to get the transcript from a YouTube video using the video id.

    Parameters
    ----------
    video_id : str
        The id of the YouTube video.

    Returns
    -------
    str
        The transcript of the video.
    """

    # Instantiate
    ytt_api = YouTubeTranscriptApi()
    
    # Fetch
    yt = ytt_api.fetch(video_id)

    # Return
    return ''.join([line.text for line in yt])


# Create agent
agent = Agent(
    model= Gemini(id="gemini-1.5-flash",
                  api_key = os.environ.get("GEMINI_API_KEY")),
                  description= "You are an assistant that summarizes YouTube videos.",
                  tools=[get_yt_transcript],
                  expected_output= "A summary of the video with the 5 main points and 2 questions for me to test my understanding.",
                  markdown=True,
                  show_tool_calls=True)


# Run agent
agent.print_response("""Summarize the text of the video with the id 'hrZSfMly_Ck' """,
                     markdown=True)


