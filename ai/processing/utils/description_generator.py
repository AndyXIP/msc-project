import os
import json
from pathlib import Path

TOP_TAGS_LIMIT = 3

def generate_descriptions(source: str, source_file: str):
    """Update JSON items by adding a description field combining caption + tags."""
    source_path = Path(source_file)

    if not source_path.exists():
        print(f"Processed JSON not found for source '{source}' at {source_path}")
        return

    with open(source_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    updated = False

    for i, item in enumerate(items):
        try:
            caption = item.get("caption", "").strip()
            tags = [tag.lower() for tag in item.get("tags", []) if tag.lower() not in caption.lower()]
            top_tags = tags[:TOP_TAGS_LIMIT]

            if top_tags:
                description = (
                    f"A hoodie design from {source} by {item.get('artist', 'unknown')}, "
                    f"featuring {caption}. Style: {', '.join(top_tags)}."
                )
            else:
                description = (
                    f"A hoodie design from {source} by {item.get('artist', 'unknown')}, "
                    f"featuring {caption}."
                )

            item["description"] = description
            updated = True

        except KeyError as e:
            print(f"Skipping item {i} in '{source}' due to missing key: {e}")

    if updated:
        with open(source_path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"[{source}] Description field added/updated in JSON.")
    else:
        print(f"[{source}] No updates made.")


def main(mode="top10"):
    prefix = "top10_" if mode == "top10" else ""

    # Load sources
    sources_file = os.path.join("data", "data_sources.json")
    if not os.path.exists(sources_file):
        print(f"Sources file not found: {sources_file}")
        return

    with open(sources_file, "r", encoding="utf-8") as f:
        sources = json.load(f)

    for source in sources:
        source_name = source.lower()
        processed_json_path = os.path.join("data", "processed", f"{prefix}{source_name}.json")
        generate_descriptions(source, processed_json_path)


if __name__ == "__main__":
    import sys
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "top10"
    if mode not in ("all", "top10"):
        print("Usage: python tag_generator.py [top10|all]")
        sys.exit(1)

    main(mode)
