use rayon::prelude::*;

const UPPER_BOUND: u64 = 5_000_000;

fn is_prime(n: u64) -> bool {
    if n < 2 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }
    let limit = (n as f64).sqrt() as u64 + 1;
    let mut i = 3;
    while i <= limit {
        if n % i == 0 {
            return false;
        }
        i += 2;
    }
    true
}

fn main() {
    let (prime_count, prime_sum): (u64, u64) = (2u64..=UPPER_BOUND)
        .into_par_iter()
        .filter(|&n| is_prime(n))
        .fold(
            || (0u64, 0u64),
            |(count, sum), n| (count + 1, sum + n),
        )
        .reduce(|| (0u64, 0u64), |(c1, s1), (c2, s2)| (c1 + c2, s1 + s2));

    println!(
        "Upper bound: {} | Cores: {} | Primes found: {} | Checksum: {}",
        UPPER_BOUND,
        rayon::current_num_threads(),
        prime_count,
        prime_sum
    );
}