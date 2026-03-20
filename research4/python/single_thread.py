import random
import sys

SAMPLES = 50_000_000


def main() -> None:
    inside = 0

    for _ in range(SAMPLES):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside += 1

    pi_estimate = 4.0 * inside / SAMPLES
    print(f"Samples: {SAMPLES} | Pi estimate: {pi_estimate:.6f} | Inside: {inside}")


if __name__ == "__main__":
    main()