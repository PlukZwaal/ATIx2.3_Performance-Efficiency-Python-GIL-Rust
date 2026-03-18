use image::imageops::FilterType;
use image::ImageError;
use std::path::{Path, PathBuf};
use std::time::Instant;
use std::{fs, process};

const INPUT_DIR: &str = "research2/images";
const OUTPUT_DIR: &str = "research2/output/rust_single";
const TARGET_W: u32 = 64;
const TARGET_H: u32 = 64;

fn process_image(src: &Path, dst: &Path) -> Result<(), ImageError> {
    let img = image::open(src)?;
    let gray = img.to_luma8();
    let resized = image::imageops::resize(&gray, TARGET_W, TARGET_H, FilterType::Nearest);
    resized.save(dst)?;
    Ok(())
}

fn main() {
    let input_dir = Path::new(INPUT_DIR);
    let output_dir = Path::new(OUTPUT_DIR);

    if !input_dir.is_dir() {
        eprintln!("Error: input directory '{}' not found.", INPUT_DIR);
        process::exit(1);
    }

    fs::create_dir_all(output_dir).expect("Failed to create output directory");

    let files: Vec<PathBuf> = fs::read_dir(input_dir)
        .expect("Failed to read input directory")
        .filter_map(|e| e.ok())
        .map(|e| e.path())
        .filter(|p| {
            matches!(
                p.extension().and_then(|e| e.to_str()),
                Some("jpg") | Some("jpeg") | Some("png")
            )
        })
        .collect();

    let total = files.len();
    let start = Instant::now();
    let mut ok: usize = 0;

    for src in &files {
        let dst = output_dir.join(src.file_name().unwrap());
        if process_image(src, &dst).is_ok() {
            ok += 1;
        }
    }

    let elapsed = start.elapsed().as_secs_f64();
    println!("Time: {:.4}s | Processed: {}/{}", elapsed, ok, total);
}
