import pandas as pd
import re
import yaml
from datetime import datetime

# --- Load Configuration ---
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

EMAIL_REGEX = config['VERIFICATION']['EMAIL_REGEX']
MIN_PHONE_LEN = config['VERIFICATION']['MIN_PHONE_LENGTH']
SHEET_TITLE = config['GOOGLE_SHEET']['SHEET_TITLE']

def verify_data(df):
    print(f"Starting verification on {len(df)} records...")
    
    # 1. Deduplication (Key Business Logic)
    df.drop_duplicates(subset=['name', 'address'], keep='first', inplace=True)
    print(f"After deduplication: {len(df)} records remain.")
    
    # 2. Basic Email Validation (Tier 1)
    df['email_verified'] = df['email_raw'].apply(
        lambda x: bool(re.match(EMAIL_REGEX, str(x)))
    )
    df_verified = df[df['email_verified'] == True].copy()
    print(f"After email validation: {len(df_verified)} records remain.")

    # 3. Phone Cleanup & Validation
    df_verified['phone_clean'] = df_verified['phone'].str.replace(r'[^0-9]', '', regex=True)
    df_verified['phone_verified'] = df_verified['phone_clean'].str.len() >= MIN_PHONE_LEN
    
    # 4. Final Output Formatting
    df_final = df_verified[df_verified['phone_verified']].copy()
    
    # Select only the clean columns for the marketplace product
    df_final = df_final[['name', 'category', 'address', 'phone', 'email_raw', 'source_url', 'scraped_date']]
    df_final.rename(columns={'email_raw': 'email'}, inplace=True)
    
    return df_final

def deliver_to_sheets(df):
    """MOCK: In a real environment, this connects to gspread and updates the Sheet."""
    print("MOCK: Connecting to Google Sheets API via stored credentials...")
    
    # --- Integration Code Placeholder ---
    # import gspread
    # gc = gspread.service_account(filename=config['GOOGLE_SHEET']['CREDENTIALS_FILE'])
    # sh = gc.open(SHEET_TITLE)
    # worksheet = sh.sheet1
    # worksheet.clear()
    # worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    # ------------------------------------
    
    print(f"MOCK: Successfully updated Google Sheet '{SHEET_TITLE}' with {len(df)} leads.")

if __name__ == "__main__":
    try:
        df_raw = pd.read_csv('data/raw/latest_raw_scrape.csv')
    except FileNotFoundError:
        print("Error: Raw scrape file not found. Run scrape_sources.py first.")
        exit()
        
    df_clean = verify_data(df_raw)
    
    # 5. Save the FINAL verified product (The core business asset)
    output_path = 'data/verified/verified_leads.csv'
    df_clean.to_csv(output_path, index=False)
    print(f"Saved verified leads to {output_path}. Ready for dashboard use.")
    
    # Optional: Deliver_to_sheets (If you choose Sheets API over Streamlit file reading)
    # deliver_to_sheets(df_clean)
