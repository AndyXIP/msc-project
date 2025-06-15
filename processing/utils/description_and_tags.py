import json
import time
import os
from dotenv import load_dotenv
from openai import OpenAI  # new import style

if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)

def generate_desc_and_tags(title, artist):
    prompt = (
        f"Write a short product description for a hoodie design titled '{title}' by artist '{artist}'. "
        "Then provide 5 relevant tags separated by commas."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.8,
        )
        text = response.choices[0].message.content.strip()
        
        if "Tags:" in text:
            description, tags_part = text.split("Tags:", 1)
            tags = [tag.strip() for tag in tags_part.split(",")]
        else:
            description = text
            tags = []
        
        return description.strip(), tags
    
    except Exception as e:
        print(f"Error generating description/tags for '{title}': {e}")
        return "", []

def enrich_data(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data):
        print(f"Processing {i+1}/{len(data)}: {item['title']}")
        description, tags = generate_desc_and_tags(item["title"], item["artist"])
        item["description"] = description
        item["tags"] = tags
        time.sleep(1)  # adjust based on rate limits

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
