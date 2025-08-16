import os
import time
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
import re

# Configuration
model_name = "runwayml/stable-diffusion-v1-5"
captions_jsonl = "data/processed/captions.jsonl"
output_dir = "./sd-finetuned-hoodie"

train_batch_size = 1
max_train_steps = 1000
learning_rate = 5e-6
resolution = 512
gradient_accumulation_steps = 2
logging_steps = 50
save_steps = 250
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

os.makedirs(output_dir, exist_ok=True)

tokenizer = CLIPTokenizer.from_pretrained(model_name, subfolder="tokenizer")

def find_latest_checkpoint(output_dir):
    unet_ckpts = []
    text_encoder_ckpts = []

    for name in os.listdir(output_dir):
        if name.startswith("unet-"):
            match = re.match(r"unet-(\d+)", name)
            if match:
                unet_ckpts.append(int(match.group(1)))
        if name.startswith("text_encoder-"):
            match = re.match(r"text_encoder-(\d+)", name)
            if match:
                text_encoder_ckpts.append(int(match.group(1)))

    if not unet_ckpts or not text_encoder_ckpts:
        return None

    latest_step = min(max(unet_ckpts), max(text_encoder_ckpts))
    return latest_step

def save_checkpoint(model, base_dir, prefix, step):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    checkpoint_dir = os.path.join(base_dir, f"{prefix}-{step}-{timestamp}")
    os.makedirs(checkpoint_dir, exist_ok=True)
    model.save_pretrained(checkpoint_dir)
    print(f"Checkpoint saved at {checkpoint_dir}")

latest_step = find_latest_checkpoint(output_dir)

if latest_step is not None:
    print(f"Found checkpoint at step {latest_step}, loading models...")
    unet = UNet2DConditionModel.from_pretrained(os.path.join(output_dir, f"unet-{latest_step}")).to(device)
    text_encoder = CLIPTextModel.from_pretrained(os.path.join(output_dir, f"text_encoder-{latest_step}")).to(device)
    global_step = latest_step
else:
    print("No checkpoint found, loading base models...")
    unet = UNet2DConditionModel.from_pretrained(model_name, subfolder="unet").to(device)
    text_encoder = CLIPTextModel.from_pretrained(model_name, subfolder="text_encoder").to(device)
    global_step = 0

vae = AutoencoderKL.from_pretrained(model_name, subfolder="vae").to(device)
vae.requires_grad_(False)
vae.eval()

transform = transforms.Compose([
    transforms.Resize((resolution, resolution), interpolation=transforms.InterpolationMode.BILINEAR),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3),
])

def preprocess(example):
    image_path = example["file_name"]
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
dataset.set_format(type="torch", columns=["pixel_values", "input_ids"])

def collate_fn(batch):
    pixel_values = torch.stack([item["pixel_values"] for item in batch])
    input_ids = torch.stack([item["input_ids"] for item in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}

dataloader = DataLoader(dataset, batch_size=train_batch_size, shuffle=True, collate_fn=collate_fn)

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

noise_scheduler = PNDMScheduler.from_pretrained(model_name, subfolder="scheduler")

print(f"Starting training from step {global_step}...")
unet.train()
text_encoder.train()

progress_bar = tqdm(total=max_train_steps)
progress_bar.update(global_step)
optimizer.zero_grad()

while global_step < max_train_steps:
    for batch in dataloader:
        pixel_values = batch["pixel_values"].to(device)
        input_ids = batch["input_ids"].to(device)

        with torch.no_grad():
            latents = vae.encode(pixel_values).latent_dist.sample() * 0.18215

        noise = torch.randn_like(latents)
        timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (latents.shape[0],), device=device).long()

        noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

        encoder_hidden_states = text_encoder(input_ids)[0]

        noise_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample

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
            save_checkpoint(unet, output_dir, "unet", global_step)
            save_checkpoint(text_encoder, output_dir, "text_encoder", global_step)

        global_step += 1
        progress_bar.update(1)

        if global_step >= max_train_steps:
            break

progress_bar.close()

save_checkpoint(unet, output_dir, "unet", "final")
save_checkpoint(text_encoder, output_dir, "text_encoder", "final")
print("Fine-tuning completed and models saved!")
