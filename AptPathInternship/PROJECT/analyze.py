import os
import google.generativeai as genai
from dotenv import load_dotenv

# Step 1: Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Step 2: Load transcript
with open("transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# Step 3: Prompt for analysis
prompt = f"""
You are analyzing a video transcript. Identify the top 3 most engaging or insightful moments with timestamps.
Output format:
1. [start_time] - [end_time]: [summary of event]

Transcript:
{transcript}
"""

# Step 4: Generate response
model = genai.GenerativeModel("gemini-1.5-pro-latest")
response = model.generate_content(prompt)

# Step 5: Output
print("\n🔍 Highlighted Segments:\n")
print(response.text)
