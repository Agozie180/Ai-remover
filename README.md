# Ai-remover

**Professional toolkit for stripping AI provenance signals and disrupting common invisible watermarks from images.**

> **Educational / Research / Authorized use only.**  
> This project helps you clean metadata and apply mild signal-disruption techniques.  
> Robust watermarks such as Google SynthID are intentionally designed to survive simple processing. Full removal of strong neural watermarks usually requires GPU-based diffusion regeneration (see related open-source projects).

## Features

- Strip AI-related metadata (EXIF, XMP, PNG text chunks, common "Made with AI" tags)
- Mild adversarial processing modes that can reduce detectability of weaker watermarks
- Clean CLI interface + Python API
- Includes a ready-to-use professional prompt for Claude, ChatGPT, Grok, Gemini, etc.
- Lightweight – no large model downloads required for basic mode

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Basic metadata cleaning
python remover.py input.png -o cleaned.png

# With light signal disruption
python remover.py input.png -o cleaned.png --mode light

# Medium disruption (slight noise + filter cycle)
python remover.py input.png -o cleaned.png --mode medium

# Batch process a folder
python remover.py ./images/ --output-dir ./cleaned/ --mode light
```

## Modes

| Mode     | Description                                      | Speed   | Visual change |
|----------|--------------------------------------------------|---------|---------------|
| `none`   | Metadata strip only                              | Fastest | None          |
| `light`  | JPEG recompression + mild sharpening             | Fast    | Very low      |
| `medium` | Light Gaussian noise + bilateral filter cycle    | Medium  | Low           |

## Professional Prompt (for Claude / ChatGPT / Grok / etc.)

See [`prompts/professional_prompt.txt`](prompts/professional_prompt.txt)

Copy-paste it when you want an AI assistant to help with advanced analysis or image editing instructions.

## Important Disclaimer

- This tool does **not** claim to fully defeat production-grade watermarks such as SynthID, StableSignature, or Tree-Ring.
- Those systems are designed to be robust against common image manipulations.
- Use only on images you own or have explicit permission to process.
- The authors are not responsible for misuse.

## Related Advanced Projects

For research-level invisible watermark removal (GPU required):
- [remove-ai-watermarks](https://github.com/wiltodelta/remove-ai-watermarks)
- [DeSynth](https://github.com/0xROOTPLS/DeSynth)
- [reverse-SynthID](https://github.com/aloshdenny/reverse-SynthID)

## License

MIT
