import json

def save_snapshot(store):
    with open("dump.json","w") as f:
        json.dump(store, f)

def load_snapshot():
    try:
        with open("dump.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}