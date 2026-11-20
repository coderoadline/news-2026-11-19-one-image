"""Deterministic renderer for the G2 entry image."""

import hashlib
import os
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"
EXPECTED = "e8d7ede40527d55acf215de7d7433170e030c506a920803be33bf7c84a17f73e"


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
