import os
import time
import re
from pathlib import Path
import platform

import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image

from datasets import load_dataset
from transformers import CLIPTokenizer, CLIPTextModel
from diffusers import AutoencoderKL, UNet2DConditionModel, PNDMScheduler, get_scheduler
from tqdm.auto import tqdm

# cuDNN autotune for speed on GPU
torch.backends.cudnn.benchmark = True


# ---------------- Configuration ---------------- #
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


# ---------------- Checkpoint Utilities ---------------- #
def find_latest_checkpoint(base_dir: str):
    """
    Finds the latest common training step across UNet and text encoder checkpoints.
    Accepts timestamped folders like 'unet-249-20250817-...' and returns actual folder paths.
    Only considers folders that contain a 'config.json'.
    """
    base = Path(base_dir)
    unet_map = {}
    txt_map = {}

    for p in base.glob("unet-*"):
        if p.is_dir() and (p / "config.json").exists():
            m = re.match(r"unet-(\d+)", p.name)
            if m:
                unet_map[int(m.group(1))] = p

    for p in base.glob("text_encoder-*"):
        if p.is_dir() and (p / "config.json").exists():
            m = re.match(r"text_encoder-(\d+)", p.name)
            if m:
                txt_map[int(m.group(1))] = p

    common_steps = sorted(set(unet_map) & set(txt_map))
    if not common_steps:
        return None
    step = common_steps[-1]
    return step, str(unet_map[step]), str(txt_map[step])


def _atomic_torch_save(obj, path: str):
    """Write a .pt atomically to avoid half-written/corrupt files on interruptions."""
    tmp = path + ".tmp"
    torch.save(obj, tmp)
    os.replace(tmp, path)


def save_checkpoint(model, base_dir, prefix, step):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    checkpoint_dir = os.path.join(base_dir, f"{prefix}-{step}-{timestamp}")
    os.makedirs(checkpoint_dir, exist_ok=True)
    model.save_pretrained(checkpoint_dir)
    print(f"Checkpoint saved at {checkpoint_dir}")
    return checkpoint_dir


def save_optimizer_scheduler(optimizer, scheduler, step, base_dir):
    _atomic_torch_save(optimizer.state_dict(), os.path.join(base_dir, f"optimizer-{step}.pt"))
    _atomic_torch_save(scheduler.state_dict(), os.path.join(base_dir, f"scheduler-{step}.pt"))


def load_optimizer_scheduler(optimizer, scheduler, step, base_dir):
    """Load optimizer/scheduler state if present and not obviously corrupt."""
    def _safe_load(path, what, apply_fn):
        if not os.path.exists(path) or os.path.getsize(path) < 1024:  # tiny/missing => skip
            print(f"[resume] {what} state not found or too small at {path}, continuing fresh.")
            return
        try:
            state = torch.load(path, map_location="cpu")
            apply_fn(state)
            print(f"[resume] loaded {what} from {path}")
        except Exception as e:
            print(f"[resume] could not load {what} ({e}), continuing fresh.")

    _safe_load(os.path.join(base_dir, f"optimizer-{step}.pt"), "optimizer", optimizer.load_state_dict)
    _safe_load(os.path.join(base_dir, f"scheduler-{step}.pt"), "scheduler", scheduler.load_state_dict)


# ---------------- Dataset utils ---------------- #
def build_transform(img_size: int):
    return transforms.Compose([
        transforms.Resize((img_size, img_size), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize([0.5] * 3, [0.5] * 3),
    ])


def preprocess_fn(example, transform, tokenizer):
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


def collate_fn(batch):
    pixel_values = torch.stack([item["pixel_values"] for item in batch])
    input_ids = torch.stack([item["input_ids"] for item in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}


def main():
    # Windows safety: ensure this code only runs once (not in worker imports)
    if platform.system() == "Windows":
        try:
            import multiprocessing as mp
            mp.freeze_support()
        except Exception:
            pass

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    os.makedirs(output_dir, exist_ok=True)

    # Tokenizer
    tokenizer = CLIPTokenizer.from_pretrained(model_name, subfolder="tokenizer")

    # Load / Resume models
    latest = find_latest_checkpoint(output_dir)
    if latest is not None:
        global_step, unet_folder, text_encoder_folder = latest
        print(f"Found checkpoint at step {global_step}, loading models...")
        unet = UNet2DConditionModel.from_pretrained(unet_folder).to(device)
        text_encoder = CLIPTextModel.from_pretrained(text_encoder_folder).to(device)
    else:
        global_step = 0
        print("No checkpoint found, loading base models...")
        unet = UNet2DConditionModel.from_pretrained(model_name, subfolder="unet").to(device)
        text_encoder = CLIPTextModel.from_pretrained(model_name, subfolder="text_encoder").to(device)

    vae = AutoencoderKL.from_pretrained(model_name, subfolder="vae").to(device)
    vae.requires_grad_(False)
    vae.eval()

    # Dataset
    transform = build_transform(resolution)
    print("Loading dataset...")
    dataset = load_dataset("json", data_files=captions_jsonl, split="train")
    dataset = dataset.map(lambda ex: preprocess_fn(ex, transform, tokenizer))
    dataset.set_format(type="torch", columns=["pixel_values", "input_ids"])
    print("Dataset size:", len(dataset), flush=True)

    # DataLoader (use num_workers=0 on Windows to avoid spawn/import issues)
    num_workers = 0 if platform.system() == "Windows" else 2
    dataloader = DataLoader(
        dataset,
        batch_size=train_batch_size,
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=num_workers,
        pin_memory=(device.type == "cuda"),
    )

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

    # Load optimizer/scheduler if resuming
    if latest is not None:
        load_optimizer_scheduler(optimizer, lr_scheduler, global_step, output_dir)

    # Noise Scheduler
    noise_scheduler = PNDMScheduler.from_pretrained(model_name, subfolder="scheduler")

    # Training Loop
    print(f"Starting training from step {global_step}...")
    unet.train()
    text_encoder.train()

    use_amp = (device.type == "cuda")
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    progress_bar = tqdm(total=max_train_steps, initial=global_step)
    optimizer.zero_grad(set_to_none=True)

    while global_step < max_train_steps:
        for batch in dataloader:
            pixel_values = batch["pixel_values"].to(device, non_blocking=True)
            input_ids = batch["input_ids"].to(device, non_blocking=True)

            # Encode to latents (no grad)
            with torch.no_grad():
                latents = vae.encode(pixel_values).latent_dist.sample() * 0.18215

            # Sample noise and timesteps
            noise = torch.randn_like(latents)
            timesteps = torch.randint(
                0,
                noise_scheduler.config.num_train_timesteps,
                (latents.shape[0],),
                device=device,
                dtype=torch.long,
            )

            # Forward + loss (AMP on GPU)
            with torch.amp.autocast("cuda", dtype=torch.float16, enabled=use_amp):
                noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)
                encoder_hidden_states = text_encoder(input_ids)[0]
                noise_pred = unet(noisy_latents, timesteps, encoder_hidden_states).sample
                loss = torch.nn.functional.mse_loss(noise_pred, noise) / gradient_accumulation_steps

            # Keep a scalar for logging before backward/scale
            loss_for_log = float(loss.detach().cpu()) * gradient_accumulation_steps

            # Backward (AMP-safe)
            if use_amp:
                scaler.scale(loss).backward()
            else:
                loss.backward()

            # Optimizer step on accumulation boundary
            if (global_step + 1) % gradient_accumulation_steps == 0:
                if use_amp:
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad(set_to_none=True)

            # Step counter then log/save so numbers match what just finished
            global_step += 1
            progress_bar.update(1)

            if global_step % logging_steps == 0:
                print(f"Step {global_step}: loss={loss_for_log:.4f}", flush=True)

            if global_step % save_steps == 0:
                save_checkpoint(unet, output_dir, "unet", global_step)
                save_checkpoint(text_encoder, output_dir, "text_encoder", global_step)
                save_optimizer_scheduler(optimizer, lr_scheduler, global_step, output_dir)

            if global_step >= max_train_steps:
                break

    progress_bar.close()

    # Save final models
    save_checkpoint(unet, output_dir, "unet", "final")
    save_checkpoint(text_encoder, output_dir, "text_encoder", "final")
    save_optimizer_scheduler(optimizer, lr_scheduler, "final", output_dir)
    print("Fine-tuning completed and models saved!")


if __name__ == "__main__":
    # Windows multiprocessing safety
    main()