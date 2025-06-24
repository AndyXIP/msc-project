import json
import os

def run_for_all_sources(process_func, raw_dir="data/raw", output_base_dir="data/processed"):
    # Determine the path to data_sources.json relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_sources_path = os.path.join(script_dir, "..", "data", "data_sources.json")

    with open(data_sources_path, "r", encoding="utf-8") as f:
        sources = json.load(f)

    raw_dir = os.path.join(script_dir, "..", raw_dir)
    output_base_dir = os.path.join(script_dir, "..", output_base_dir)

    for source in sources:
        input_path = os.path.join(raw_dir, f"{source}.json")
        output_path = os.path.join(output_base_dir, source)
        print(f"Processing {source}...")
        process_func(input_path, output_path)
        print(f"Finished {source}.\n")
