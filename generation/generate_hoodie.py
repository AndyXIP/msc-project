import torch
from diffusers import StableDiffusionPipeline, PNDMScheduler
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import AutoencoderKL, UNet2DConditionModel
import os

def load_model(model_dir="./sd-finetuned-model"):
    print("Loading fine-tuned model...")
    unet = UNet2DConditionModel.from_pretrained(os.path.join(model_dir, "unet"))
    text_encoder = CLIPTextModel.from_pretrained(os.path.join(model_dir, "text_encoder"))
    vae = AutoencoderKL.from_pretrained("runwayml/stable-diffusion-v1-5", subfolder="vae")
    tokenizer = CLIPTokenizer.from_pretrained("runwayml/stable-diffusion-v1-5", subfolder="tokenizer")

    scheduler = PNDMScheduler.from_pretrained("runwayml/stable-diffusion-v1-5", subfolder="scheduler")

    pipe = StableDiffusionPipeline(
        vae=vae,
        text_encoder=text_encoder,
        tokenizer=tokenizer,
        unet=unet,
        scheduler=scheduler,
        safety_checker=None,
        feature_extractor=None,
    )
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    print(f"Model loaded on {device}")
    return pipe

def get_next_filename(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    existing_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
    existing_numbers = []
    for f in existing_files:
        name, _ = os.path.splitext(f)
        if name.isdigit():
            existing_numbers.append(int(name))
    next_number = max(existing_numbers, default=0) + 1
    return os.path.join(output_dir, f"{next_number}.png")

def generate_image(pipe, prompt, output_path=None, height=512, width=512, guidance_scale=7.5, num_inference_steps=50):
    print(f"Generating image for prompt: {prompt}")
    image = pipe(prompt, height=height, width=width, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps).images[0]

    if output_path is None:
        output_path = get_next_filename("data/images/generated")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    image.save(output_path)
    print(f"Saved image at {output_path}")

def batch_generate(pipe, prompts, output_dir="data/images/generated"):
    os.makedirs(output_dir, exist_ok=True)
    for prompt in prompts:
        output_path = get_next_filename(output_dir)
        generate_image(pipe, prompt, output_path)

if __name__ == "__main__":
    pipe = load_model()

    # Generate a single image
    single_prompt = "A hoodie design featuring a futuristic cat with space background, graphic design style"
    generate_image(pipe, single_prompt)  # saves as data/generated/1.png or next available

    # Generate a batch of images
    batch_prompts = [
        "A hoodie design with abstract shapes and neon colors, cyberpunk style",
        "A hoodie design showing a fantasy dragon in a mystical forest",
        "A hoodie design inspired by retro video games, pixel art style",
    ]
    batch_generate(pipe, batch_prompts)
