import os
import sys
from pathlib import Path


ASSET = Path(__file__).resolve().parent / "assets" / "entry.png"


def main() -> int:
    """Copy the bundled poster to the output directory the runner expects."""
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_path = output_dir / "entry.png"

    if not ASSET.is_file():
        print(f"error: missing asset {ASSET}", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(ASSET.read_bytes())
    print(output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
