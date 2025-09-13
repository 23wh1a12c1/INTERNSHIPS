import whisper

model = whisper.load_model("base")
result = model.transcribe("test.wav")

print("✅ Transcription complete!")
print("Transcribed Text:")
print(result["text"])

# Save to files
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

import json
with open("segments.json", "w", encoding="utf-8") as f:
    json.dump(result["segments"], f, indent=2)
