import os
import time
from PIL import Image

# Configuration
INPUT_DIR = os.path.join("research2", "images")
OUTPUT_DIR = os.path.join("research2", "output", "python_single")

def process_images():
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Get list of images
    try:
        image_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    except FileNotFoundError:
        print(f"Error: Input directory '{INPUT_DIR}' not found.")
        return

    start_time = time.time()
    success_count = 0
    
    for filename in image_files:
        try:
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename)
            
            with Image.open(input_path) as img:
                # Convert to 8-bit Grayscale ('L')
                img_gray = img.convert("L")
                # Resize to 64x64 using NEAREST resampling
                img_resized = img_gray.resize((64, 64), Image.NEAREST)
                # Save
                img_resized.save(output_path)
                
            success_count += 1
        except Exception:
            # Skip corrupted images without crashing
            continue
            
    end_time = time.time()
    
    print(f"Total time: {end_time - start_time:.4f} seconds")
    print(f"Successfully processed: {success_count}")

if __name__ == "__main__":
    process_images()
