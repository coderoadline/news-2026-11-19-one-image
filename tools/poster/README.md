# World News Poster Generator (19 November 2026)

This tool generates the canonical 1024×1024 editorial world news poster for the `news-image-20261119` competition on make.fun.

## Requirements

- **Chromium** (headless mode): `/usr/bin/chromium`
- **Python 3.10+**
- **Pillow** (`PIL`) for validation and checksums
- System Western fonts: `Nimbus Roman`, `Nimbus Sans`, `DejaVu Serif`, `DejaVu Sans`

## Structure

- `index.html`: Complete editorial broadsheet layout formatted in HTML/CSS with embedded SVG assets.
- `generate.py`: Headless Chromium renderer producing deterministic 1024×1024 PNG output.
- `README.md`: Reproduction documentation and technical specification.

## How to Re-generate

Run the generator script directly from this directory or repository root:

```bash
# Render to default destination (repo/assets/entry.png)
python3 repo/tools/poster/generate.py

# Or specify a custom output path
python3 repo/tools/poster/generate.py --output /path/to/custom_entry.png
```

## Determinism & Verification

The poster relies exclusively on local vector assets and system fonts, guaranteeing bit-for-bit rendering determinism across successive runs without network dependencies.
