import pandas as pd
import re
import yaml
import os
from datetime import datetime
# Removed the unnecessary 'from bs4 import BeautifulSoup' import

# --- Load Configuration ---
try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config/config.yaml not found.")
    exit(1)

EMAIL_REGEX = config['VERIFICATION']['EMAIL_REGEX']
# Using MIN_PHONE_LENGTH as verified in the configuration
MIN_PHONE_LEN = config['VERIFICATION']['MIN_PHONE_LENGTH'] 

def verify_data(df):
    print(f"Starting verification on {len(df)} records...")
    
    # 1. Deduplication (Using the new, reliable key columns)
    df.drop_duplicates(subset=['Business Name', 'City'], keep='first', inplace=True)
    
    # 2. Basic Email Validation (Tier 1 - Using the correct 'Email' column)
    df['email_verified'] = df['Email'].apply(
        lambda x: bool(re.match(EMAIL_REGEX, str(x)))
    )
    df_verified = df[df['email_verified'] == True].copy()
    
    # 3. Phone Cleanup & Validation (Using the correct 'Phone' column)
    df_verified['phone_clean'] = df_verified['Phone'].astype(str).str.replace(r'[^0-9]', '', regex=True)
    df_verified['phone_verified'] = df_verified['phone_clean'].str.len() >= MIN_PHONE_LEN
    
    # 4. Final Output Filtering and Formatting
    df_final = df_verified[
        (df_verified['phone_verified']) & 
        (df_verified['email_verified'])
    ].copy()
    
    # List of all expected columns for the dashboard's enrichment
    expected_cols = [
        'Business Name', 'Phone', 'Email', 'City', 'Niche', 'Lead Score', 
        'Reason to Contact', 'Attribute', 'source_url', 'scraped_date'
    ]
    
    # Filter the final DataFrame to only include these columns
    cols_to_keep = [col for col in expected_cols if col in df_final.columns]
    df_final = df_final[cols_to_keep]
    
    print(f"Final verified lead count: {len(df_final)}")
    return df_final

# --------------------------------------------------
# MAIN WORKFLOW EXECUTION (CRITICAL: Only runs the verifier)
# --------------------------------------------------

if __name__ == "__main__":
    try:
        raw_file_path = 'data/raw/latest_raw_scrape.csv'
        if not os.path.exists(raw_file_path):
             raise FileNotFoundError("Raw scrape file missing. Ensure scripts/scrape_sources.py ran successfully.")
            
        df_raw = pd.read_csv(raw_file_path)
        
        # FIX 1: Explicitly cast the new capitalized columns to string
        # This prevents the 'phone' KeyError and subsequent type errors
        # This must match the output of scrape_sources.py exactly!
        df_raw['Phone'] = df_raw['Phone'].astype(str)
        df_raw['Email'] = df_raw['Email'].astype(str)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        # Catch the KeyError if the column names are still wrong or missing
        if "KeyError" in str(e):
             print(f"Critical Error: Column names missing in raw data. Check scraper output! Details: {e}")
        else:
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
        # Write headers based on the final expected columns for stability
        expected_cols_final = [
            'Business Name', 'Phone', 'Email', 'City', 'Niche', 'Lead Score', 
            'Reason to Contact', 'Attribute', 'source_url', 'scraped_date'
        ]
        pd.DataFrame(columns=expected_cols_final).to_csv(output_path, index=False)
        print("Warning: No verified leads were generated. Wrote empty headers.")
