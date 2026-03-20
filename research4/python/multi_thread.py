import random
import os
from concurrent.futures import ThreadPoolExecutor

SAMPLES = 50_000_000


def count_inside(samples: int) -> int:
    rng = random.Random()  # eigen instantie per thread — voorkomt lock contention op de globale RNG
    inside = 0
    for _ in range(samples):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return inside


def main() -> None:
    num_cpus = os.cpu_count() or 1
    chunk_size = SAMPLES // num_cpus
    chunks = [chunk_size] * num_cpus
    # verdeel resterende samples over het eerste chunk
    chunks[0] += SAMPLES - sum(chunks)

    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        results = list(executor.map(count_inside, chunks))

    inside = sum(results)
    pi_estimate = 4.0 * inside / SAMPLES
    print(f"Samples: {SAMPLES} | Cores: {num_cpus} | Pi estimate: {pi_estimate:.6f} | Inside: {inside}")


if __name__ == "__main__":
    main()