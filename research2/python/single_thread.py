import os
import sys
import time
from pathlib import Path
from PIL import Image

INPUT_DIR  = Path("research2/images")
OUTPUT_DIR = Path("research2/output/python_single")

EXTENSIONS = {".jpg", ".jpeg", ".png"}
TARGET_SIZE = (64, 64)


def process_image(src: Path, dst: Path) -> bool:
    try:
        with Image.open(src) as img:
            result = img.convert("L").resize(TARGET_SIZE, Image.NEAREST)
            result.save(dst)
        return True
    except Exception:
        return False


def main() -> None:
    if not INPUT_DIR.is_dir():
        print(f"Error: input directory '{INPUT_DIR}' not found.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = [p for p in INPUT_DIR.iterdir() if p.suffix.lower() in EXTENSIONS]

    start = time.perf_counter()
    ok = 0

    for src in files:
        dst = OUTPUT_DIR / src.name
        if process_image(src, dst):
            ok += 1

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed:.4f}s | Processed: {ok}/{len(files)}")


if __name__ == "__main__":
    main()