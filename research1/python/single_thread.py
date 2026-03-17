import csv
import sys

def calculate_complexity(text):
    score = 0
    for char in text:
        score += (ord(char) ** 2) % 12345
    return score

def main():
    filename = "research1/dataset.csv"
    total_rows = 0
    total_complexity = 0
    
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_rows += 1
                text = row['Text']
                total_complexity += calculate_complexity(text)
                
        print(f"Rows: {total_rows} | Checksum: {total_complexity}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()