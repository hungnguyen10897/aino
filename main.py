from openai import OpenAI
import time, sys, os
from assistant import *
from utils import *
from voice import text_to_speech, get_prompt_from_speech

API_KEY=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def submit_message(assistant_id, thread, user_message):
  client.beta.threads.messages.create(
      thread_id=thread.id, role="user", content=user_message
  )
  return client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant_id,
  )

def get_latest_response(thread):
  messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=2)
  return messages.data[0].content[0].text.value

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def create_thread_and_run(assistant_id, user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

if __name__ == "__main__":

  # Create or Retrieve Assistant
  if sys.argv[1] == "-c":
    assistant = create_assistant(client)
  elif len(sys.argv[1]) >= 2:
    assistant_id = sys.argv[1]
    assistant = retrieve_assistant(client, assistant_id)

  text_to_speech(client, "Hi! I'm Aino. How may I help you?\n")
  first_prompt = get_prompt_from_speech(client)

  print(f"Prompt: {first_prompt}")

  thread, run0 = create_thread_and_run(assistant.id, first_prompt)
  
  # Wait till it's finished
  run0 = wait_on_run(run0, thread)
  response = get_latest_response(thread)
  print(f"Reponse: {response}")
  text_to_speech(client, response)

  while True:
    prompt = get_prompt_from_speech(client)

    print(f"Prompt: {prompt}")

    if prompt.lower() == "end":
      break
     
    runN = submit_message(assistant.id, thread, prompt)
    runN = wait_on_run(runN, thread)

    reponse = get_latest_response(thread)
    print(f"Reponse: {reponse}")
    text_to_speech(client, reponse)
    
