import os
import json

def save_to_json(data, fname):
    directory = "./data/raw/"
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
    filename = os.path.join(directory, fname)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
