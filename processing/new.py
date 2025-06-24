from utils.description_and_tags import enrich_data
from utils.process_all_data import run_for_all_sources
import os

def enrich_data_wrapper(input_path, output_path):
    processed_file = output_path + "_processed.json"
    enrich_data(input_path, processed_file)

if __name__ == "__main__":
    run_for_all_sources(enrich_data_wrapper, raw_dir="data/raw", output_base_dir="data/processed")
