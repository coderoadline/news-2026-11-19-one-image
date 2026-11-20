"""Deterministic renderer for the E6 entry image."""

import hashlib
import os
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"
EXPECTED = "d45520476b9603bf27b8fd2e8943e318a18a398ca7008a1bdcb26e1a7c976c97"


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
