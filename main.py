from openai import OpenAI
import time, sys, os
from assistant import *
from utils import *
from voice import get_prompt_from_speech2, stream_text_to_speech
from assistant import *

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

_timing = True
debug = False

if __name__ == "__main__":

  # Create or Retrieve Assistant
  if sys.argv[1] == "-c":
    assistant = create_assistant(client)
  elif len(sys.argv[1]) >= 2:
    assistant_id = sys.argv[1]
    assistant = retrieve_assistant(client, assistant_id)

  # stream_text_to_speech(client, "Hi! I'm Ismo. How may I help you?\n", timing=_timing)
  stream_text_to_speech(client, "Hi! I'm Aino. How may I help you?\n", timing=_timing)

  first_prompt = get_prompt_from_speech2(client, timing=_timing)
  if debug:
    print(f"Prompt: {first_prompt}")
  
  if _timing:
    start_time=time.time()
  thread, run0 = create_thread_and_run(client, assistant.id, first_prompt)
  
  # Wait till it's finished
  run0 = wait_on_run(client, run0, thread)
  response = get_latest_response(client, thread)
  if debug:
    print(f"Reponse: {response}")
  if _timing:
    print("---Dead Time - first_openai_call: {:.2f} seconds".format(time.time() - start_time))

  stream_text_to_speech(client, response, timing=_timing)

  while True:
    prompt = get_prompt_from_speech2(client, timing=_timing)
    if debug:
      print(f"Prompt: {prompt}")
    if prompt.lower() == "end":
      break
    
    if _timing:
       start_time=time.time()
    runN = submit_message(client, assistant.id, thread, prompt)
    
    if _timing:
      print("---Dead Time - submit_message: {:.2f} seconds".format(time.time() - start_time))
      start_time=time.time()

    runN = wait_on_run(client, runN, thread)

    if _timing:
      print("---Dead Time - wait_on_run: {:.2f} seconds".format(time.time() - start_time))
      start_time=time.time()

    reponse = get_latest_response(client, thread)

    if _timing:
      print("---Dead Time - get_latest_response: {:.2f} seconds".format(time.time() - start_time))
      start_time=time.time()
    
    if debug:
      print(f"Reponse: {reponse}")

    stream_text_to_speech(client, reponse, timing=_timing)
