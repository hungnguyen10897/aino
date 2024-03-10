from pvrecorder import PvRecorder
import struct, wave
from playsound import playsound

recorder = PvRecorder(device_index=-1, frame_length=512)
prompt_file_path = "temp/_prompt.mp3"

def text_to_speech(client, text):
  response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
  )
  response.stream_to_file("temp/_response.mp3")
  playsound("temp/_response.mp3")

def get_prompt_from_speech(client):
  # Recording
  audio = []

  try:
    print("Listening...")
    recorder.start()

    while True:
      frame = recorder.read()
      # Do something ...
      audio.extend(frame)
  except KeyboardInterrupt:
    recorder.stop()
    print("Listening stopped")
    with wave.open(prompt_file_path, 'w') as f:
      f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
      f.writeframes(struct.pack("h" * len(audio), *audio))

  prompt_file= open(prompt_file_path, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=prompt_file
  )
  return transcription.text

def get_microphones():
  for index, device in enumerate(PvRecorder.get_audio_devices()):
    print(f"[{index}] {device}")
