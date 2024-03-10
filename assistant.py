from configs import *

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
