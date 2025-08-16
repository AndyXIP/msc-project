import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import json
from pathlib import Path
from mimetypes import guess_type

router = APIRouter()

HOODIE_FOLDER = "data/images"
DB_PATH = "data/hoodies.json"

def load_hoodies():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_hoodies(hoodies):
    with open(DB_PATH, "w") as f:
        json.dump(hoodies, f, indent=2)

@router.get("/hoodies")
async def list_hoodies():
    return load_hoodies()

@router.get("/hoodies/image/{category}/{image_name}")
async def get_hoodie_image(category: str, image_name: str):
    if category not in ("generated", "original"):
        raise HTTPException(status_code=400, detail="Invalid category")

    hoodies = load_hoodies()
    found_path = None

    for hoodie in hoodies:
        image_field = "ai_image_url" if category == "generated" else "original_image_url"
        image_url = hoodie.get(image_field)
        if not image_url:
            continue

        filename = Path(image_url).name
        if filename == image_name:
            found_path = os.path.join(HOODIE_FOLDER, category, image_name)
            break

    if not found_path or not os.path.exists(found_path):
        raise HTTPException(status_code=404, detail="Image not found")

    mime_type, _ = guess_type(found_path)
    return FileResponse(found_path, media_type=mime_type or "application/octet-stream")
 