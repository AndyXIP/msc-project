import json
import easyocr
import os

# ---------- CONFIG ----------
input_folder = "data/processed"
input_files = [
    "top10_redbubble.json",
    "top10_society6.json",
    "top10_threadless.json"
]
max_items_per_file = 10
# ----------------------------

# Initialize OCR reader (English only here, can add more langs)
reader = easyocr.Reader(['en'])

def has_text(image_path, min_chars=3):
    """Return True if OCR detects text in the image."""
    if not image_path or not os.path.exists(image_path):
        print(f"⚠️ File not found: {image_path}")
        return False  # Treat missing files as "no text"
    results = reader.readtext(image_path)
    extracted_text = " ".join([res[1] for res in results])
    return len(extracted_text.strip()) >= min_chars


# Process each JSON file
for file_name in input_files:
    file_path = os.path.join(input_folder, file_name)

    if not os.path.exists(file_path):
        print(f"⚠️ JSON file not found: {file_path}")
        continue

    # Load JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    filtered_data = []
    for item in data:
        if len(filtered_data) >= max_items_per_file:
            break  # Stop once we have 10 items

        image_path = item.get("local_image_url")
        cropped_path = item.get("local_cropped_url")

        # Check both image paths
        if (image_path and has_text(image_path)) or (cropped_path and has_text(cropped_path)):
            print(f"❌ Skipping {image_path} / {cropped_path} (text detected)")
        else:
            print(f"✅ Keeping {image_path} / {cropped_path} (no text)")
            filtered_data.append(item)

    # Overwrite JSON file with filtered content (max 10 items)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 {file_name}: Kept {len(filtered_data)} items "
          f"(removed {len(data) - len(filtered_data)} with text).\n")
