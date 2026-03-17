use csv::Reader;
use rayon::prelude::*;
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

    let mut rdr = match Reader::from_path(filename) {
        Ok(r) => r,
        Err(_) => {
            println!("Error: {} not found!", filename);
            process::exit(1);
        }
    };

    // Determine column index by name so it matches Python's row['Text'] behaviour
    let headers = rdr.headers()?.clone();
    let text_idx = headers
        .iter()
        .position(|h| h == "Text")
        .unwrap_or_else(|| {
            eprintln!("Warning: 'Text' column not found, falling back to index 0");
            0
        });

    let records: Vec<_> = rdr.records().collect::<Result<Vec<_>, _>>()?;
    let total_rows = records.len();

    let total_complexity: i64 = records
        .par_iter()
        .map(|record| {
            if let Some(text) = record.get(text_idx) {
                calculate_complexity(text)
            } else {
                0
            }
        })
        .sum();

    println!("Rows: {} | Checksum: {}", total_rows, total_complexity);
    Ok(())
}