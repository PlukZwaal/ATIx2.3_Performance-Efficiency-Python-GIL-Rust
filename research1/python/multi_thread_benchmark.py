import csv
import sys
import os
from concurrent.futures import ThreadPoolExecutor

def calculate_complexity(text):
    score = 0
    for char in text:
        score += (ord(char) ** 2) % 12345
    return score

def process_chunk(rows):
    chunk_score = 0
    for row in rows:
        text = row['Text']
        chunk_score += calculate_complexity(text)
    return chunk_score

def main():
    filename = "research1/dataset.csv"
    num_cpus = os.cpu_count() or 1
    all_rows = []

    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            all_rows = list(reader)
        
        total_rows = len(all_rows)
        chunk_size = max(1, total_rows // num_cpus)
        chunks = [all_rows[i:i + chunk_size] for i in range(0, total_rows, chunk_size)]

        with ThreadPoolExecutor(max_workers=num_cpus) as executor:
            results = list(executor.map(process_chunk, chunks))
            total_complexity = sum(results)

        print(f"Cores: {num_cpus} | Rows: {total_rows} | Checksum: {total_complexity}")

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()