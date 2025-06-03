from youtube_transcript_api import YouTubeTranscriptApi

# Instantiate
ytt_api = YouTubeTranscriptApi()

# Fetch
yt = ytt_api.fetch('T-y5Y-t-dmc')
# Return

t = {}
for line in yt:
    t[line.start] = {'text': line.text}
    
print(t)