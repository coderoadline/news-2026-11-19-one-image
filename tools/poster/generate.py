#!/usr/bin/env python3
"""
World News Poster Generator for make.fun 'news-image-20261119'
Renders index.html to 1024x1024 PNG using headless Chromium.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path


def render_poster(html_path: Path, output_path: Path) -> dict:
    chromium_bin = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not chromium_bin:
        raise RuntimeError("Chromium binary not found on system.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        chromium_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--force-device-scale-factor=1",
        "--window-size=1024,1024",
        f"--screenshot={output_path.resolve()}",
        f"file://{html_path.resolve()}",
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if not output_path.is_file():
        raise RuntimeError(f"Screenshot failed. Stderr: {res.stderr}")

    import PIL.Image

    with PIL.Image.open(output_path) as im:
        width, height = im.size
        img_format = im.format

    file_size = output_path.stat().st_size
    sha256_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()

    # Validation
    if (width, height) != (1024, 1024):
        raise ValueError(f"Invalid dimensions: {width}x{height}, expected 1024x1024")
    if img_format != "PNG":
        raise ValueError(f"Invalid format: {img_format}, expected PNG")
    if file_size > 1024 * 1024:
        raise ValueError(f"File size {file_size} exceeds 1 MiB limit")

    return {
        "output_path": str(output_path),
        "dimensions": (width, height),
        "format": img_format,
        "bytes": file_size,
        "sha256": sha256_hash,
    }


def main():
    parser = argparse.ArgumentParser(description="Render 1024x1024 news poster PNG")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "assets" / "entry.png",
        help="Target output PNG path",
    )
    args = parser.parse_args()

    current_dir = Path(__file__).resolve().parent
    html_file = current_dir / "index.html"

    result = render_poster(html_file, args.output)
    print(f"Generated: {result['output_path']}")
    print(f"Dimensions: {result['dimensions'][0]}x{result['dimensions'][1]}")
    print(f"Format: {result['format']}")
    print(f"Bytes: {result['bytes']}")
    print(f"SHA-256: {result['sha256']}")


if __name__ == "__main__":
    main()
