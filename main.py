import shutil
import struct
import zlib
from pathlib import Path


def _generate_placeholder_png(target_path: Path) -> None:
    width = 1024
    height = 1024
    color_rgb = (26, 32, 44)

    png = bytearray(b"\x89PNG\r\n\x1a\n")

    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data)
    png.extend(struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc))

    row_bytes = b"\x00" + bytes(color_rgb) * width
    raw_data = row_bytes * height
    compressed = zlib.compress(raw_data, 9)
    idat_crc = zlib.crc32(b"IDAT" + compressed)
    png.extend(struct.pack(">I", len(compressed)) + b"IDAT" + compressed + struct.pack(">I", idat_crc))

    iend_crc = zlib.crc32(b"IEND")
    png.extend(struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc))

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(png)


def main() -> None:
    repo_dir = Path(__file__).resolve().parent
    assets_entry = repo_dir / "assets" / "entry.png"
    output_entry = Path("/output/entry.png")

    output_entry.parent.mkdir(parents=True, exist_ok=True)

    if assets_entry.is_file():
        shutil.copyfile(assets_entry, output_entry)
    else:
        _generate_placeholder_png(output_entry)


if __name__ == "__main__":
    main()
