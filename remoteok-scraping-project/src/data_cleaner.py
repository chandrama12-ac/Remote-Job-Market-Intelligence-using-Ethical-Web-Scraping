import pandas as pd
import os
from datetime import datetime

class DataCleaner:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def clean_data(self):
        if not os.path.exists(self.input_path):
            print(f"Error: {self.input_path} not found.")
            return

        import csv
        print(f"Reading raw data from {os.path.abspath(self.input_path)}...")
        try:
            with open(self.input_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            df = pd.DataFrame(data)
        except Exception as e:
            print(f"Critical Error reading CSV: {e}")
            return

        initial_len = len(df)
        
        # 1. Remove exact duplicates based on Job URL
        df.drop_duplicates(subset=['Job URL'], keep='first', inplace=True)
        
        # 2. Handle missing values
        df['Job Title'] = df['Job Title'].fillna('Unknown Title')
        df['Company Name'] = df['Company Name'].fillna('Unknown Company')
        df['Location'] = df['Location'].fillna('Remote')
        df['Job Tags'] = df['Job Tags'].fillna('')
        
        # 3. Process Date Posted
        # RemoteOK uses ISO format (e.g., 2023-11-20T...) or relative strings
        # We'll try to convert to YYYY-MM-DD
        def parse_date(date_str):
            try:
                if pd.isna(date_str) or date_str == 'N/A':
                    return datetime.now().strftime('%Y-%m-%d')
                # Try parsing standard ISO
                return pd.to_datetime(date_str).strftime('%Y-%m-%d')
            except:
                return datetime.now().strftime('%Y-%m-%d')

        df['Date Posted'] = df['Date Posted'].apply(parse_date)

        # 4. Normalize Job Title (Title Case)
        df['Job Title'] = df['Job Title'].str.title().str.strip()
        
        # 5. Normalize Company Name
        df['Company Name'] = df['Company Name'].str.strip()

        print(f"Cleaning complete. Reduced rows from {initial_len} to {len(df)}.")
        
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        df.to_csv(self.output_path, index=False, encoding='utf-8-sig')
        print(f"Saved cleaned data to {self.output_path}")

if __name__ == "__main__":
    # Locate project root relative to this file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    raw_csv = os.path.join(project_root, "data", "raw", "remoteok_raw.csv")
    cleaned_csv = os.path.join(project_root, "data", "cleaned", "remoteok_jobs_cleaned.csv")
    cleaner = DataCleaner(raw_csv, cleaned_csv)
    cleaner.clean_data()
