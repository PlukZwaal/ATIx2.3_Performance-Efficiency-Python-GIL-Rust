import math
import sys

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


def main() -> None:
    prime_count = 0
    prime_sum = 0

    for n in range(2, UPPER_BOUND + 1):
        if is_prime(n):
            prime_count += 1
            prime_sum += n

    print(f"Upper bound: {UPPER_BOUND} | Primes found: {prime_count} | Checksum: {prime_sum}")


if __name__ == "__main__":
    main()