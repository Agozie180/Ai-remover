#!/usr/bin/env python3
"""
Ai-remover – Robust mode
Diffusion-based regeneration for hard invisible watermarks (SynthID-class).
Requires: torch + diffusers + controlnet_aux + NVIDIA GPU recommended.
"""

import argparse
from pathlib import Path
import torch
from PIL import Image
import numpy as np

from diffusers import (
    StableDiffusionXLControlNetImg2ImgPipeline,
    ControlNetModel,
    AutoencoderKL,
)
from diffusers.utils import load_image
from controlnet_aux import CannyDetector


def strip_metadata(img: Image.Image) -> Image.Image:
    data = list(img.getdata())
    clean = Image.new(img.mode, img.size)
    clean.putdata(data)
    clean.info = {}
    return clean


def main():
    parser = argparse.ArgumentParser(description="Robust AI watermark remover (diffusion)")
    parser.add_argument("input", type=str, help="Input image")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output image")
    parser.add_argument("--strength", type=float, default=0.22,
                        help="Denoise strength (0.15–0.35 recommended). Higher = stronger removal, more change")
    parser.add_argument("--steps", type=int, default=28, help="Inference steps")
    parser.add_argument("--guidance", type=float, default=3.5, help="Guidance scale")
    parser.add_argument("--controlnet-scale", type=float, default=0.85,
                        help="How strongly to follow Canny edges (0.7–0.95)")
    parser.add_argument("--device", type=str, default="auto",
                        help="cuda / cpu / auto")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    device = args.device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Device: {device}")
    print(f"Strength: {args.strength} | Steps: {args.steps}")

    # Load image
    init_image = load_image(args.input).convert("RGB")
    init_image = strip_metadata(init_image)

    # Canny condition
    canny = CannyDetector()
    control_image = canny(init_image, low_threshold=100, high_threshold=200)
    control_image = control_image.resize(init_image.size)

    print("Loading models (first run downloads ~6-8 GB)...")

    controlnet = ControlNetModel.from_pretrained(
        "diffusers/controlnet-canny-sdxl-1.0",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )

    vae = AutoencoderKL.from_pretrained(
        "madebyollin/sdxl-vae-fp16-fix",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )

    pipe = StableDiffusionXLControlNetImg2ImgPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        controlnet=controlnet,
        vae=vae,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        variant="fp16" if device == "cuda" else None,
    )

    if device == "cuda":
        pipe.enable_model_cpu_offload()
        # pipe.enable_xformers_memory_efficient_attention()  # optional if available
    else:
        pipe = pipe.to(device)

    generator = torch.Generator(device=device).manual_seed(args.seed)

    print("Running regeneration...")
    result = pipe(
        prompt="high quality, detailed, sharp, natural photograph",
        negative_prompt="blurry, low quality, artifacts, watermark, text, logo",
        image=init_image,
        control_image=control_image,
        strength=args.strength,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        controlnet_conditioning_scale=args.controlnet_scale,
        generator=generator,
    ).images[0]

    # Final clean save
    result = strip_metadata(result)
    result.save(args.output, quality=95)
    print(f"✓ Robust cleaned image saved → {args.output}")


if __name__ == "__main__":
    main()
