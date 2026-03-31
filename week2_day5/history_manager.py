import json
import os

HISTORY_FILE = "weather_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE,"r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
        
    return []

def save_history(history):
    with open(HISTORY_FILE,"w") as file:
        json.dump(history, file, indent=4)