"""Deterministic renderer for the F1 entry image."""

import hashlib
import os
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"
EXPECTED = "d994254a4f9873c5e18768dc533641b18f994e1c4ac636104a97039ab6492606"


def main():
    try:
        if not ASSET.is_file():
            raise FileNotFoundError(f"missing asset: {ASSET}")
        data = ASSET.read_bytes()
        if hashlib.sha256(data).hexdigest() != EXPECTED:
            raise ValueError("asset sha256 mismatch")
        output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / "entry.png"
        output.write_bytes(data)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
