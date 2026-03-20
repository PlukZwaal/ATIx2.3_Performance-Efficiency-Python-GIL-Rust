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
    let mut prime_count: u64 = 0;
    let mut prime_sum: u64 = 0;

    for n in 2..=UPPER_BOUND {
        if is_prime(n) {
            prime_count += 1;
            prime_sum += n;
        }
    }

    println!(
        "Upper bound: {} | Primes found: {} | Checksum: {}",
        UPPER_BOUND, prime_count, prime_sum
    );
}