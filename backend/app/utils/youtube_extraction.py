# YouTube Extraction utility (migrated from old mcq_env)
# Migrated the YouTube transcript extraction utility from the old mcq_env project to the new backend utils folder. This enables extracting text from YouTube videos for MCQ generation.

import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(youtube_url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

def extract_transcript_from_youtube(youtube_url):
    video_id = get_video_id(youtube_url)
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = " ".join([d["text"] for d in transcript_list])
    return transcript
