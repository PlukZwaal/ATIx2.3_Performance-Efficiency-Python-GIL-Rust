use csv::Reader;
use std::error::Error;
use std::process;

fn calculate_complexity(text: &str) -> i64 {
    let mut score: i64 = 0;
    for c in text.chars() {
        score += ((c as i64).pow(2)) % 12345;
    }
    score
}

fn main() -> Result<(), Box<dyn Error>> {
    let filename = "research1/dataset.csv";
    let mut total_rows = 0;
    let mut total_complexity: i64 = 0;

    let mut rdr = match Reader::from_path(filename) {
        Ok(r) => r,
        Err(_) => {
            println!("Error: {} not found!", filename);
            process::exit(1);
        }
    };

    for result in rdr.records() {
        let record = result?;
        if let Some(text) = record.get(0) {
            total_rows += 1;
            total_complexity += calculate_complexity(text);
        }
    }

    println!("Rows: {} | Checksum: {}", total_rows, total_complexity);
    Ok(())
}