use rand::Rng;

const SAMPLES: u64 = 50_000_000;

fn main() {
    let mut rng = rand::rng();
    let mut inside: u64 = 0;

    for _ in 0..SAMPLES {
        let x: f64 = rng.random();
        let y: f64 = rng.random();
        if x * x + y * y <= 1.0 {
            inside += 1;
        }
    }

    let pi_estimate = 4.0 * inside as f64 / SAMPLES as f64;
    println!(
        "Samples: {} | Pi estimate: {:.6} | Inside: {}",
        SAMPLES, pi_estimate, inside
    );
}