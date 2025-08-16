import os
import json

def save_to_json(data, fname):
    # Get directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build path relative to this script
    directory = os.path.join(script_dir, "..", "..", "data", "raw")
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists

    filename = os.path.join(directory, fname)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(data)} items to {filename}")
