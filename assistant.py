from configs import *
import time

def create_assistant(client):
  assistant = client.beta.assistants.create(
    name="Aino",
    instructions=ASSISTANT_INSTRUCTIONS,
    model="gpt-3.5-turbo-0125",
  )
  return assistant

def retrieve_assistant(client, assistant_id):
  assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
  return assistant

def submit_message(client, assistant_id, thread, user_message):
  client.beta.threads.messages.create(
      thread_id=thread.id, role="user", content=user_message
  )
  return client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant_id,
  )

def get_latest_response(client, thread):
  messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=2)
  return messages.data[0].content[0].text.value

def wait_on_run(client, run, thread):
  while run.status == "queued" or run.status == "in_progress":
      run = client.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id,
      )
      time.sleep(0.5)
  return run

def create_thread_and_run(client, assistant_id, user_input):
  thread = client.beta.threads.create()
  run = submit_message(client, assistant_id, thread, user_input)
  return thread, run
