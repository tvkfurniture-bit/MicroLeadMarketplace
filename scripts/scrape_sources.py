import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import yaml
import re
import os # CRITICAL FIX: Ensures os module is available for directory creation

# --- Load Configuration ---
# Ensure you have a valid config/config.yaml file
try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config/config.yaml not found.")
    exit(1)

SCRAPE_CITY = config['SCRAPING_CONFIG']['PRIMARY_CITY']

def fetch_data_from_directory(query):
    """
    MOCK FUNCTION: Simulates pulling structured data from a source.
    (This is where Playwright/Selenium would go in a production setup.)
    """
    print(f"--- Scraping data for: {query} in {SCRAPE_CITY} ---")
    
    scraped_leads = []
    for i in range(1, 10): 
        scraped_leads.append({
            'name': f"Business Alpha {i}",
            'category': query,
            'address': f"{i*10} Main St, {SCRAPE_CITY}",
            'phone': f"+1 555-123-{1000 + i}",
            # Use real-looking emails that PASS basic regex for stable pipeline testing
            'email_raw': f"test.alpha{i}@servicecorp.com", 
            'source_url': f"http://source.com/lead_{i}",
            'scraped_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        time.sleep(random.uniform(0.1, 0.5)) 

    return pd.DataFrame(scraped_leads)

if __name__ == "__main__":
    df_raw = fetch_data_from_directory(config['SCRAPING_CONFIG']['PRIMARY_NICHE'])
    
    # Ensure raw directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    # Save raw data
    df_raw.to_csv('data/raw/latest_raw_scrape.csv', index=False)
    print(f"Scraped {len(df_raw)} raw records.")
