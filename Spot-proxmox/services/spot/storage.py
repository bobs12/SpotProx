import json
from config import DATA_FILE

def load_instances():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_instances(instances):
    with open(DATA_FILE, "w") as f:
        json.dump(instances, f, indent=2)
