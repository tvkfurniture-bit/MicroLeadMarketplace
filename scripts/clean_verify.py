import pandas as pd
import re
import yaml
import os
from datetime import datetime

# --- Load Configuration ---
try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config/config.yaml not found.")
    exit(1)

EMAIL_REGEX = config['VERIFICATION']['EMAIL_REGEX']
MIN_PHONE_LEN = config['VERIFICATION']['MIN_PHONE_LENGTH']

def verify_data(df):
    print(f"Starting verification on {len(df)} records...")
    
    # 1. Deduplication (Key Business Logic)
    df.drop_duplicates(subset=['name', 'address'], keep='first', inplace=True)
    
    # 2. Basic Email Validation (Tier 1)
    df['email_verified'] = df['email_raw'].apply(
        lambda x: bool(re.match(EMAIL_REGEX, str(x)))
    )
    df_verified = df[df['email_verified'] == True].copy()
    
    # 3. Phone Cleanup & Validation
    df_verified['phone_clean'] = df_verified['phone'].astype(str).str.replace(r'[^0-9]', '', regex=True)
    df_verified['phone_verified'] = df_verified['phone_clean'].str.len() >= MIN_PHONE_LEN
    
    # 4. Final Output Formatting (Only include records verified for both)
    df_final = df_verified[
        (df_verified['phone_verified']) & 
        (df_verified['email_verified'])
    ].copy()
    
    # Select only the clean columns for the marketplace product
    df_final = df_final[['name', 'category', 'address', 'phone', 'email_raw', 'source_url', 'scraped_date']]
    df_final.rename(columns={'email_raw': 'email'}, inplace=True)
    
    print(f"Final verified lead count: {len(df_final)}")
    return df_final

if __name__ == "__main__":
    try:
        raw_file_path = 'data/raw/latest_raw_scrape.csv'
        if not os.path.exists(raw_file_path):
             # Ensure the scraper ran successfully before proceeding
             raise FileNotFoundError("Raw scrape file missing. Ensure scripts/scrape_sources.py ran successfully.")
            
        df_raw = pd.read_csv(raw_file_path)
        
        # Explicitly cast columns to string to prevent validation errors
        df_raw['phone'] = df_raw['phone'].astype(str)
        df_raw['email_raw'] = df_raw['email_raw'].astype(str)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Critical error during data loading or casting: {e}")
        exit(1)
        
    df_clean = verify_data(df_raw)
    
    # Ensure the verified directory exists
    os.makedirs('data/verified', exist_ok=True)
    
    # Save the FINAL verified product (The core business asset)
    output_path = 'data/verified/verified_leads.csv'
    
    if not df_clean.empty:
        df_clean.to_csv(output_path, index=False)
        print(f"Successfully saved verified leads to {output_path}.")
    else:
        # Crucial for stability: If empty, write only headers to avoid "File Not Found" errors in Streamlit
        pd.DataFrame(columns=['name', 'category', 'address', 'phone', 'email', 'source_url', 'scraped_date']).to_csv(output_path, index=False)
        print("Warning: No verified leads were generated. Wrote empty headers.")
