from openai import OpenAI
import time, sys, os
from assistant import *
from utils import *
from voice import text_to_speech, get_prompt_from_speech, get_prompt_from_speech2
from assistant import *

API_KEY=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

timing = True
debug = False

if __name__ == "__main__":

  # Create or Retrieve Assistant
  if sys.argv[1] == "-c":
    assistant = create_assistant(client)
  elif len(sys.argv[1]) >= 2:
    assistant_id = sys.argv[1]
    assistant = retrieve_assistant(client, assistant_id)

  text_to_speech(client, "Hi! I'm Ismo. How may I help you?\n", timing=True)

  first_prompt = get_prompt_from_speech2(client, timing=True)
  if debug:
    print(f"Prompt: {first_prompt}")
  
  if timing:
    start_time=time.time()
  thread, run0 = create_thread_and_run(client, assistant.id, first_prompt)
  
  # Wait till it's finished
  run0 = wait_on_run(client, run0, thread)
  response = get_latest_response(client, thread)
  if debug:
    print(f"Reponse: {response}")
  if timing:
    print("---Dead Time - first_openap_call: {:.2f} seconds".format(time.time() - start_time))


  text_to_speech(client, response, timing=True)

  while True:
    prompt = get_prompt_from_speech2(client, timing=True)
    if debug:
      print(f"Prompt: {prompt}")
    if prompt.lower() == "end":
      break
    
    if timing:
       start_time=time.time()
    runN = submit_message(client, assistant.id, thread, prompt)
    runN = wait_on_run(client, runN, thread)

    reponse = get_latest_response(client, thread)
    
    if debug:
      print(f"Reponse: {reponse}")
    if timing:
      print("---Dead Time - get_response_from_openai: {:.2f} seconds".format(time.time() - start_time))

    text_to_speech(client, reponse, timing=True)
