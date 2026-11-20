import hashlib
import os
import sys
from pathlib import Path

ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"
EXPECTED = "5b37f1d642f44fddc15630dee44c121ae5e478f874e9fe0f4c69efbc8b181c0e"


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main():
    try:
        if not ASSET.is_file():
            raise FileNotFoundError(f"missing asset: {ASSET}")
        if digest(ASSET) != EXPECTED:
            raise ValueError("asset sha256 mismatch")
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
