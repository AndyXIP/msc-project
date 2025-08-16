import os
import requests
from PIL import Image
from io import BytesIO

def download_image(url, source, filename):
    base_dir = "data/images"
    output_dir = os.path.join(base_dir, source)
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img.save(filepath)

        print(f"Saved image to {filepath}")
        return filepath

    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None
