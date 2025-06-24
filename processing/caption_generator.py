import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import re

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def clean_caption(caption):
    # Regex to remove leading subject + preposition like "a man wearing", "a woman in", etc.
    pattern = r'^(a|the)?\s*(man|woman|person|someone|girl|boy|human|people)?\s*(wearing|in|with)\s+'
    cleaned = re.sub(pattern, '', caption, flags=re.IGNORECASE)
    return cleaned.strip()

def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return clean_caption(caption)


def main():
    caption = generate_caption("data/images/redbubble/100.jpg")
    print("Caption:", caption)

if __name__ == "__main__":
    main()