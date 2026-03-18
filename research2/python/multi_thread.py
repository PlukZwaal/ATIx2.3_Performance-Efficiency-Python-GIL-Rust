import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import only the module; each worker opens its own Image object
# so no Pillow state is shared across threads — safe with and without the GIL.
from PIL import Image

INPUT_DIR  = Path("research2/images")
OUTPUT_DIR = Path("research2/output/python_multi")

EXTENSIONS  = {".jpg", ".jpeg", ".png"}
TARGET_SIZE = (64, 64)


def process_image(src: Path, dst: Path) -> bool:
    """
    Completely self-contained per-task function.
    No shared mutable objects → safe for Python 3.13t (free-threaded).
    """
    try:
        # Open, convert, resize and save are all done inside this scope.
        # The Image object is never passed between threads.
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

    # Use all available logical CPUs; on 3.13t this truly runs in parallel.
    num_workers = os.cpu_count() or 1

    start = time.perf_counter()
    ok = 0

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(process_image, src, OUTPUT_DIR / src.name): src
            for src in files
        }
        for future in as_completed(futures):
            if future.result():
                ok += 1

    elapsed = time.perf_counter() - start
    print(f"Time: {elapsed:.4f}s | Processed: {ok}/{len(files)} | Workers: {num_workers}")


if __name__ == "__main__":
    main()