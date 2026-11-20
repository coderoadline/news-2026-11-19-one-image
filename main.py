import hashlib
import os
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"
EXPECTED = "7681e9ff32d86ddea8aba47ea5c3eeeb3ed92c3b558a62b82f8639da998d6fcd"


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main():
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output = output_dir / "entry.png"
    try:
        if not ASSET.is_file():
            print(f"error: missing asset: {ASSET}", file=sys.stderr)
            return 1
        if digest(ASSET) != EXPECTED:
            print("error: asset sha256 mismatch", file=sys.stderr)
            return 1
        data = ASSET.read_bytes()
        if hashlib.sha256(data).hexdigest() != EXPECTED:
            print("error: asset sha256 mismatch", file=sys.stderr)
            return 1
        output_dir.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
        print(output)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
