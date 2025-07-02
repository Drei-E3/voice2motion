import json

def load_environment(path="environment.json"):
    with open(path, 'r') as f:
        return json.load(f)