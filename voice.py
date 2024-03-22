import speech_recognition as sr
from playsound import playsound
from pvrecorder import PvRecorder
import struct, wave, time
import configs as cfg

recorder = PvRecorder(device_index=-1, frame_length=512)

r = sr.Recognizer()
r.pause_threshold = cfg.PAUSE_THRESHOLD
prompt_file_path = "temp/_prompt.mp3"

def text_to_speech(client, text, timing = False):
  if timing:
    start_time = time.time()
  response = client.audio.speech.create(
    model="tts-1",
    voice=cfg.VOICE,
    input=text
  )
  response.stream_to_file("temp/_response.mp3")
  if timing:
    print("---Dead Time - text_to_speech(): {:.2f} seconds".format(time.time() - start_time))
  playsound("temp/_response.mp3")
  

def get_prompt_from_speech(client):

  with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
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

def get_prompt_from_speech2(client, timing = False):
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

    if timing:
      start_time = time.time()
    with wave.open(prompt_file_path, 'w') as f:
      f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
      f.writeframes(struct.pack("h" * len(audio), *audio))

  prompt_file= open(prompt_file_path, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=prompt_file
  )
  if timing:
    print("---Dead Time - get_prompt_from_speech2(): {:.2f} seconds".format(time.time() - start_time))
  return transcription.text

def get_microphones():
  for index, device in enumerate(PvRecorder.get_audio_devices()):
    print(f"[{index}] {device}")
