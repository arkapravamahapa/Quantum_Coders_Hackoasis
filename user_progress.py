import json
import os

PROGRESS_FILE = "data/user_progress.json"

def load_progress():
    """
    Load the user's progress from disk if it exists.
    Returns an empty dict if no progress file is found.
    """
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_progress(progress_data):
    """
    Save the given progress data to disk,
    creating the folder if it doesn’t exist yet.
    """
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress_data, f, indent=4)

def export_progress():
    """
    Return the user's progress as a nicely formatted JSON string.
    """
    return json.dumps(load_progress(), indent=4)
