import clip
import torch
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)

def generate_tags(image_path, candidate_tags, top_k=5):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # Encode image
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    
    # Encode candidate tags
    text = clip.tokenize(candidate_tags).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
    
    # Compute cosine similarity
    similarity = (image_features @ text_features.T).squeeze(0)
    
    # Get top k tags
    values, indices = similarity.topk(top_k)
    tags = [candidate_tags[i] for i in indices]
    return tags

def main():
    tags_list = [
        # Product types
        "hoodie", "sweatshirt", "pullover", "zip-up", "crewneck", "long sleeve", "graphic tee",
        
        # Colors (basic and common ones)
        "black", "white", "gray", "red", "blue", "green", "yellow", "navy", "pink", "purple",
        
        # Styles / patterns
        "casual", "sporty", "plain", "striped", "checkered", "graphic", "logo", "printed", "embroidered",
        
        # Audience
        "men's", "women's", "unisex", "kids",
        
        # Features
        "front print", "zipper", "pockets", "hooded", "lightweight", "heavyweight", "fleece", "cotton"
    ]

    tags = generate_tags("data/images/redbubble/0.jpg", tags_list)
    print("Tags:", tags)

if __name__ == "__main__":
    main()