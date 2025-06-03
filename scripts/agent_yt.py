# Imports
import os
from agno.agent import Agent
from agno.models.google import Gemini
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
                  instructions= ["Break down the concepts of the video into 5 main points",
                                 "Create analogies for me to teach my students",
                                 "Create 2 questions for me to test my students understanding"],
                  tools=[get_yt_transcript],
                  expected_output= "A summary of the video with the 5 main points and 2 questions",
                  markdown=True,
                  show_tool_calls=True)


# Run agent
prompt = """Summarize the text of the video with the id 'pg19Z8LL06w' """	
agent.print_response(prompt, markdown=True)


