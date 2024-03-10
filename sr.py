import os
import speech_recognition as sr
from openai import OpenAI

r = sr.Recognizer()

r.pause_threshold = 5

API_KEY=os.environ("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

print("Say Something")

with sr.Microphone() as source:
  r.adjust_for_ambient_noise(source)
  print("Listening")
  audio = r.listen(source, timeout=10)
  print("Listening ended")

with open(f"temp/test_output.wav", "wb") as f:
  f.write(audio.get_wav_data())

# prompt_file= open(prompt_file_path, "rb")
with open(f"temp/test_output.wav", "rb") as f:
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=f
  )

  print(f"S2T: {transcription.text}")