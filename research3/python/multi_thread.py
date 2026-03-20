import math
import os
import sys
from concurrent.futures import ThreadPoolExecutor

UPPER_BOUND = 5_000_000


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def process_chunk(start: int, end: int) -> tuple[int, int]:
    """Return (count, sum) of primes in [start, end)."""
    count = 0
    total = 0
    for n in range(start, end):
        if is_prime(n):
            count += 1
            total += n
    return count, total


def main() -> None:
    num_cpus = os.cpu_count() or 1
    chunk_size = max(1, UPPER_BOUND // num_cpus)

    ranges = [
        (i, min(i + chunk_size, UPPER_BOUND + 1))
        for i in range(2, UPPER_BOUND + 1, chunk_size)
    ]

    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        results = list(executor.map(lambda r: process_chunk(*r), ranges))

    prime_count = sum(c for c, _ in results)
    prime_sum = sum(s for _, s in results)

    print(f"Upper bound: {UPPER_BOUND} | Cores: {num_cpus} | Primes found: {prime_count} | Checksum: {prime_sum}")


if __name__ == "__main__":
    main()