import pandas as pd
import re
import os

def is_english(text):
    # Simple heuristic to detect English: 
    # Check if the string contains only ASCII characters commonly used in English
    try:
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def clean_and_filter():
    input_path = os.path.join('stage_01_data', 'reviews_raw.csv')
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    print(f"Initial reviews: {len(df)}")

    # 0. Date filtering (Last 8-12 weeks)
    df['Date'] = pd.to_datetime(df['Date'])
    cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=84) # 12 weeks
    df = df[df['Date'] >= cutoff_date]
    print(f"Reviews in last 12 weeks: {len(df)}")

    # 1. Remove Title field
    if 'Title' in df.columns:
        df = df.drop(columns=['Title'])
        print("Removed 'Title' column.")

    # 2. Remove reviews with 5 or fewer words
    df = df[df['Review'].str.split().str.len() > 5]
    print(f"Reviews after length filter (> 5 words): {len(df)}")

    # 3. Remove non-English reviews
    df = df[df['Review'].apply(is_english)]
    print(f"Reviews after language filter (English only): {len(df)}")

    # Save cleaned data
    output_path = os.path.join('stage_02_processing', 'reviews_cleaned.csv')
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to {output_path}")

if __name__ == "__main__":
    clean_and_filter()
