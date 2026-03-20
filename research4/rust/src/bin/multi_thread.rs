use rand::Rng;
use rayon::prelude::*;

const SAMPLES: u64 = 50_000_000;

fn main() {
    let inside: u64 = (0..SAMPLES)
        .into_par_iter()
        .map(|_| {
            let mut rng = rand::rng();
            let x: f64 = rng.random();
            let y: f64 = rng.random();
            if x * x + y * y <= 1.0 { 1u64 } else { 0u64 }
        })
        .sum();

    let pi_estimate = 4.0 * inside as f64 / SAMPLES as f64;
    println!(
        "Samples: {} | Cores: {} | Pi estimate: {:.6} | Inside: {}",
        SAMPLES,
        rayon::current_num_threads(),
        pi_estimate,
        inside
    );
}