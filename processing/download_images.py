from utils.image_download import download_images_from_json
from utils.process_all_data import run_for_all_sources

def download_images_wrapper(input_path, output_path):
    # output_path here is a directory (e.g. data/images/redbubble)
    # make sure directory exists
    os.makedirs(output_path, exist_ok=True)
    download_images_from_json(input_path, output_path)

if __name__ == "__main__":
    run_for_all_sources(download_images_wrapper, raw_dir="data/raw", output_base_dir="data/images")
