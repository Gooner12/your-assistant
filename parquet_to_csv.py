import os
import pandas as pd
import csv

# Define the directory containing Parquet files

def get_paths():
    base_path = os.path.abspath(".")
    parquet_path = r"ragtest\output\20240719-085223\artifacts"
    csv_path = r"csv\output\20240719-085223"
    csv_dir = os.path.join(base_path, csv_path)
    parquet_dir = os.path.join(base_path, parquet_path)
    return parquet_dir, csv_dir

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

parquet_dir, csv_dir = get_paths()
create_directory(csv_dir)       

# parquet_dir = '/Users/test/graphrag/inputs/artifacts'
# csv_dir = '/Users/test/graphrag/neo4j-community-5.21.2/import'

# Function to clean and properly format the string fields
def clean_quotes(value):
    if isinstance(value, str):
        # Remove extra quotes and strip leading/trailing spaces
        value = value.strip().replace('""', '"').replace('"', '')
        # Ensure proper quoting for fields with commas or quotes
        if ',' in value or '"' in value:
            value = f'"{value}"'
    return value

# Convert all Parquet files to CSV
for file_name in os.listdir(parquet_dir):
    if file_name.endswith('.parquet'):
        parquet_file = os.path.join(parquet_dir, file_name)
        csv_file = os.path.join(csv_dir, file_name.replace('.parquet', '.csv'))
        
        # Load the Parquet file
        df = pd.read_parquet(parquet_file)
        
        # Clean quotes in string fields
        for column in df.select_dtypes(include=['object']).columns:
            df[column] = df[column].apply(clean_quotes)
        
        # Save to CSV
        df.to_csv(csv_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
        print(f"Converted {parquet_file} to {csv_file} successfully.")

print("All Parquet files have been converted to CSV.")