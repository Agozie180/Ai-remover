# Ai-remover

**Professional toolkit for removing AI provenance signals and the hardest invisible watermarks (including SynthID-class marks).**

> **Educational / Research / Authorized use only.**  
> Use only on images you own or have explicit permission to process.

## Two Levels of Removal

| Level | Method | GPU | Best for |
|-------|--------|-----|----------|
| **Basic** | Metadata stripping + mild signal disruption | No | Fast cleanup, weaker marks |
| **Robust** (recommended) | Diffusion regeneration (img2img + ControlNet) | NVIDIA GPU strongly recommended | Hardest / most robust watermarks (SynthID, StableSignature, Tree-Ring, etc.) |

---

## 1. Basic Mode (lightweight)

```bash
pip install -r requirements.txt
python remover.py input.png -o cleaned.png --mode medium
```

Modes: `none` | `light` | `medium`

---

## 2. Robust Mode – Hardest Watermarks (Docker recommended)

This is the mode you want for the strongest current invisible watermarks.

### Option A – One-command Docker (easiest)

```bash
# Build once
docker build -t ai-remover .

# Run (NVIDIA GPU)
docker run --gpus all --rm -v $(pwd):/data ai-remover \
  robust /data/your_image.png -o /data/cleaned.png --strength 0.22

# CPU only (much slower)
docker run --rm -v $(pwd):/data ai-remover \
  robust /data/your_image.png -o /data/cleaned.png --strength 0.22 --device cpu
```

### Option B – Native Ubuntu / local install

```bash
# Requires NVIDIA drivers + CUDA toolkit
pip install -r requirements-robust.txt

python robust_remover.py your_image.png -o cleaned.png --strength 0.22
```

### Recommended strength values (start here)

| Goal                        | `--strength` | Notes                          |
|----------------------------|--------------|--------------------------------|
| Maximum fidelity           | 0.15–0.18    | May need 2 passes on stubborn marks |
| Balanced (recommended)     | 0.20–0.25    | Best starting point            |
| Aggressive / stubborn marks| 0.28–0.35    | More visual change             |

You can also run multiple low-strength passes for better quality:

```bash
python robust_remover.py img.png -o tmp1.png --strength 0.18
python robust_remover.py tmp1.png -o cleaned.png --strength 0.18
```

---

## How the Robust pipeline works

1. Strips all metadata / C2PA / EXIF
2. Extracts Canny edges for structure preservation
3. Runs controlled diffusion regeneration (img2img + ControlNet)
4. Reconstructs the image so the invisible watermark pattern is disrupted while keeping composition and style as close as possible

This is the same core technique used by current research-grade open-source SynthID bypass tools.
---

## Hardware Notes

- **Best experience**: NVIDIA GPU with ≥ 10–12 GB VRAM
- First run downloads models (~6–8 GB)
- CPU works but is very slow

---

## Disclaimer

No open method is guaranteed against every future version of proprietary watermarks. Results vary by image content, resolution, and the exact watermark implementation. Always verify with the vendor’s detector when possible.

This project is for research, education, and legitimate use on content you control.

## License

MIT
