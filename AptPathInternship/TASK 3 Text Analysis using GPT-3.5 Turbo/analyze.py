
import os
from dotenv import load_dotenv
import google.generativeai as genai



# Load API Key from .env
load_dotenv()
api_key = os.getenv("AIzaSyAN06sY5nq7nfu1iixGg-zZxUQumEsICPY")

genai.configure(api_key='AIzaSyAN06sY5nq7nfu1iixGg-zZxUQumEsICPY')

# Load transcript
with open("transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

prompt = f"""
You are analyzing a video transcript. Identify the top 3-5 most engaging or insightful moments with their timestamps.
Format the output like this:

1. [start_time] - [end_time]: [summary]
2. ...

Transcript:
{transcript}
"""

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content(prompt)

# Display output
print("🎯 Smart Reel Moments:")
print(response.text)

# Optionally save output
with open("highlights.txt", "w", encoding="utf-8") as f:
    f.write(response.text)
