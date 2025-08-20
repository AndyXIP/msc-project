from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

DB_PATH = "data/hoodies.json"


def load_hoodies():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=404, detail="Hoodies database not found")

    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/hoodies")
async def list_hoodies():
    return load_hoodies()
