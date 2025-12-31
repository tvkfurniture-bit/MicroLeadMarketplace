import pandas as pd
import re
import yaml
import os
from datetime import datetime

# --- Load Configuration ---
# NOTE: The PATH for config.yaml assumes this script is run from the project root
# (as it is by GitHub Actions).
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

EMAIL_REGEX = config['VERIFICATION']['EMAIL_REGEX']
MIN_PHONE_LEN = config['VERIFICATION']['MIN_PHONE_LENGTH']

def verify_data(df):
    print(f"Starting verification on {len(df)} records...")
    
    # 1. Deduplication (Key Business Logic)
    df.drop_duplicates(subset=['name', 'address'], keep='first', inplace=True)
    print(f"After deduplication: {len(df)} records remain.")
    
    # 2. Basic Email Validation (Tier 1 - RE-ENABLED)
    df['email_verified'] = df['email_raw'].apply(
        lambda x: bool(re.match(EMAIL_REGEX, str(x)))
    )
    # Filter the leads that have valid email syntax
    df_verified = df[df['email_verified'] == True].copy() 
    print(f"After email validation: {len(df_verified)} records remain.")
    
    # 3. Phone Cleanup & Validation
    df_verified['phone_clean'] = df_verified['phone'].astype(str).str.replace(r'[^0-9]', '', regex=True)
    df_verified['phone_verified'] = df_verified['phone_clean'].str.len() >= MIN_PHONE_LEN
    
    # 4. Final Output Formatting (Only include leads that passed all quality checks)
    df_final = df_verified[df_verified['phone_verified']].copy()
    
    # Select only the clean columns for the marketplace product
    df_final = df_final[['name', 'category', 'address', 'phone', 'email_raw', 'source_url', 'scraped_date']]
    df_final.rename(columns={'email_raw': 'email'}, inplace=True)
    
    print(f"Final verified lead count: {len(df_final)}")
    return df_final

if __name__ == "__main__":
    try:
        # NOTE: Using a relative path that works because the GA workflow runs from the root
        df_raw = pd.read_csv('data/raw/latest_raw_scrape.csv')
        
        # Ensure critical columns are strings before cleanup
        df_raw['phone'] = df_raw['phone'].astype(str)
        df_raw['email_raw'] = df_raw['email_raw'].astype(str)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
        
    df_clean = verify_data(df_raw)
    
    # Ensure the verified directory exists
    os.makedirs('data/verified', exist_ok=True)
    
    # Save the FINAL verified product
    output_path = 'data/verified/verified_leads.csv'
    df_clean.to_csv(output_path, index=False)
    print(f"Successfully saved verified leads to {output_path}.")
