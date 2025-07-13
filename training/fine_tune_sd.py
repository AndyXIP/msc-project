import os
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image
from datasets import load_dataset
from transformers import CLIPTokenizer, CLIPTextModel
from diffusers import (
    AutoencoderKL,
    UNet2DConditionModel,
    PNDMScheduler,
    get_scheduler,
)
from tqdm.auto import tqdm

# Configuration
model_name = "runwayml/stable-diffusion-v1-5"
captions_jsonl = "data/processed/captions.jsonl"
output_dir = "./sd-finetuned-hoodie"

train_batch_size = 1
max_train_steps = 2000
learning_rate = 5e-6
resolution = 512
gradient_accumulation_steps = 2
logging_steps = 50
save_steps = 500
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

os.makedirs(output_dir, exist_ok=True)

# Load tokenizer and models
tokenizer = CLIPTokenizer.from_pretrained(model_name, subfolder="tokenizer")
text_encoder = CLIPTextModel.from_pretrained(model_name, subfolder="text_encoder").to(device)
vae = AutoencoderKL.from_pretrained(model_name, subfolder="vae").to(device)
unet = UNet2DConditionModel.from_pretrained(model_name, subfolder="unet").to(device)

# Freeze VAE parameters
vae.requires_grad_(False)
vae.eval()

# Image transform: resize, to tensor, normalize to [-1, 1]
transform = transforms.Compose([
    transforms.Resize((resolution, resolution), interpolation=transforms.InterpolationMode.BILINEAR),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3),
])

# Dataset preprocessing function
def preprocess(example):
    image_path = example["file_name"]  # full path in JSONL
    image = Image.open(image_path).convert("RGB")
    image = transform(image)
    example["pixel_values"] = image

    inputs = tokenizer(
        example["text"],
        padding="max_length",
        max_length=tokenizer.model_max_length,
        truncation=True,
        return_tensors="pt",
    )
    example["input_ids"] = inputs.input_ids.squeeze(0)
    return example

print("Loading dataset...")
dataset = load_dataset("json", data_files=captions_jsonl, split="train")
dataset = dataset.map(preprocess)

# IMPORTANT: Set dataset format for PyTorch tensors
dataset.set_format(type="torch", columns=["pixel_values", "input_ids"])

def collate_fn(batch):
    pixel_values = torch.stack([item["pixel_values"] for item in batch])
    input_ids = torch.stack([item["input_ids"] for item in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}

dataloader = DataLoader(dataset, batch_size=train_batch_size, shuffle=True, collate_fn=collate_fn)

# Optimizer & Scheduler
optimizer = torch.optim.AdamW(
    list(unet.parameters()) + list(text_encoder.parameters()),
    lr=learning_rate,
    betas=(0.9, 0.999),
    weight_decay=0.01,
)

lr_scheduler = get_scheduler(
    "linear",
    optimizer=optimizer,
    num_warmup_steps=0,
    num_training_steps=max_train_steps,
)

# Use PNDMScheduler for noise schedule (matches original SD)
noise_scheduler = PNDMScheduler.from_pretrained(model_name, subfolder="scheduler")

print("Starting training...")
unet.train()
text_encoder.train()

global_step = 0
progress_bar = tqdm(total=max_train_steps)

optimizer.zero_grad()

while global_step < max_train_steps:
    for batch in dataloader:
        pixel_values = batch["pixel_values"].to(device)
        input_ids = batch["input_ids"].to(device)

        # Encode images to latents
        with torch.no_grad():
            latents = vae.encode(pixel_values).latent_dist.sample() * 0.18215

        # Sample noise and timesteps
        noise = torch.randn_like(latents)
        timesteps = torch.randint(0, noise_scheduler.num_train_timesteps, (latents.shape[0],), device=device).long()

        # Add noise to latents
        noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

        # Get text embeddings
        encoder_hidden_states = text_encoder(input_ids)[0]

        # Predict noise residual
        noise_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample

        # Calculate loss (MSE)
        loss = torch.nn.functional.mse_loss(noise_pred, noise)
        loss = loss / gradient_accumulation_steps
        loss.backward()

        if (global_step + 1) % gradient_accumulation_steps == 0:
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()

        if global_step % logging_steps == 0:
            tqdm.write(f"Step {global_step}: loss={loss.item() * gradient_accumulation_steps:.4f}")

        if (global_step + 1) % save_steps == 0:
            unet.save_pretrained(os.path.join(output_dir, f"unet-{global_step}"))
            text_encoder.save_pretrained(os.path.join(output_dir, f"text_encoder-{global_step}"))
            print(f"Checkpoint saved at step {global_step}")

        global_step += 1
        progress_bar.update(1)

        if global_step >= max_train_steps:
            break

progress_bar.close()

# Save final models
unet.save_pretrained(os.path.join(output_dir, "unet"))
text_encoder.save_pretrained(os.path.join(output_dir, "text_encoder"))
print("Fine-tuning completed and models saved!")
