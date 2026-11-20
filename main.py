import hashlib
import os
import sys
from pathlib import Path


ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"
EXPECTED = "88dbdd5fcce723f610f96a94d5663cb88ccdd16c2796c091889da091b24082a1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_path = output_dir / "entry.png"
    try:
        if not ASSET.is_file():
            print(f"error: missing asset: {ASSET}", file=sys.stderr)
            return 1
        if sha256(ASSET) != EXPECTED:
            print("error: asset sha256 mismatch", file=sys.stderr)
            return 1
        data = ASSET.read_bytes()
        if hashlib.sha256(data).hexdigest() != EXPECTED:
            print("error: asset sha256 mismatch", file=sys.stderr)
            return 1
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(data)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
