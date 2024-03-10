import json

# Pretty printing helper
def pretty_print(messages):
    # print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

def show_json(obj):
  print(json.dumps(json.loads(obj.model_dump_json()), indent=4))
