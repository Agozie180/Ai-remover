#!/usr/bin/env python3
"""
Ai-remover – Lightweight AI provenance cleaner & mild watermark disruptor
Educational / research use only.
"""

import argparse
import os
from pathlib import Path
from typing import Optional

from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

try:
    import piexif
    HAS_PIEXIF = True
except ImportError:
    HAS_PIEXIF = False


def strip_metadata(img: Image.Image) -> Image.Image:
    """Remove EXIF and other metadata while keeping pixel data."""
    data = list(img.getdata())
    clean = Image.new(img.mode, img.size)
    clean.putdata(data)

    # Explicitly clear any remaining info
    clean.info = {}
    return clean


def apply_light(img: Image.Image) -> Image.Image:
    """Light disruption: mild sharpen + high-quality JPEG cycle."""
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.15)

    # Force a JPEG recompression cycle (breaks some fragile signals)
    from io import BytesIO
    buffer = BytesIO()
    img.convert("RGB").save(buffer, format="JPEG", quality=93, optimize=True)
    buffer.seek(0)
    return Image.open(buffer).convert(img.mode if img.mode != "RGB" else "RGB")


def apply_medium(img: Image.Image) -> Image.Image:
    """Medium disruption: controlled noise + bilateral-style smoothing."""
    arr = np.array(img).astype(np.float32)

    # Very mild Gaussian noise
    noise = np.random.normal(0, 1.8, arr.shape).astype(np.float32)
    arr = np.clip(arr + noise, 0, 255)

    img = Image.fromarray(arr.astype(np.uint8))

    # Light bilateral-like filtering via successive box + median
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = img.filter(ImageFilter.SMOOTH_MORE)

    # Tiny contrast boost to restore punch
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.04)

    return img


def process_image(
    input_path: Path,
    output_path: Path,
    mode: str = "none",
) -> None:
    img = Image.open(input_path)

    # Always strip metadata first
    img = strip_metadata(img)

    if mode == "light":
        img = apply_light(img)
    elif mode == "medium":
        img = apply_medium(img)

    # Final save without any metadata
    save_kwargs = {}
    if output_path.suffix.lower() in {".jpg", ".jpeg"}:
        save_kwargs = {"quality": 95, "optimize": True}
        img = img.convert("RGB")

    img.save(output_path, **save_kwargs)
    print(f"✓ Cleaned → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Ai-remover – Strip AI metadata and mildly disrupt invisible watermarks"
    )
    parser.add_argument("input", type=str, help="Input image or directory")
    parser.add_argument("-o", "--output", type=str, help="Output file (for single image)")
    parser.add_argument(
        "--output-dir", type=str, default="cleaned",
        help="Output directory when processing a folder"
    )
    parser.add_argument(
        "--mode",
        choices=["none", "light", "medium"],
        default="none",
        help="Disruption strength (default: none = metadata only)"
    )

    args = parser.parse_args()
    input_path = Path(args.input)

    if input_path.is_file():
        out = Path(args.output) if args.output else input_path.with_stem(input_path.stem + "_cleaned")
        process_image(input_path, out, args.mode)
    elif input_path.is_dir():
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        extensions = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
        for f in input_path.iterdir():
            if f.suffix.lower() in extensions:
                out_file = out_dir / f.name
                process_image(f, out_file, args.mode)
    else:
        print("Error: input must be a file or directory")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
