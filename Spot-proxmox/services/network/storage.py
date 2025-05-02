import json
from config import DATA_FILE


def load_network():
    try:
        with open (DATA_FILE, r) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}