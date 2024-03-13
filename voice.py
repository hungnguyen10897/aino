import speech_recognition as sr
from playsound import playsound
from pvrecorder import PvRecorder

r = sr.Recognizer()
r.pause_threshold = 3
prompt_file_path = "temp/_prompt.mp3"

def text_to_speech(client, text):
  response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text
  )
  response.stream_to_file("temp/_response.mp3")
  playsound("temp/_response.mp3")

def get_prompt_from_speech(client):

  with sr.Microphone() as source:
    # r.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = r.listen(source, timeout=10)
    print("Listening ended")

  with open(prompt_file_path, "wb") as f:
    f.write(audio.get_wav_data())

  prompt_file= open(prompt_file_path, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=prompt_file
  )
  return transcription.text

def get_microphones():
  for index, device in enumerate(PvRecorder.get_audio_devices()):
    print(f"[{index}] {device}")
