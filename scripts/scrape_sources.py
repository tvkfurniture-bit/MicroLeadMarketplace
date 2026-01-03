import pandas as pd
import time
import random
import yaml
import os
from datetime import datetime
import gspread # CRITICAL: GSheets library
import json # CRITICAL: JSON handling for the secret

# --- CONFIGURATION & PATHS ---
try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config/config.yaml not found.")
    exit(1)

# Paths for the workflow
RAW_OUTPUT_PATH = 'data/raw/latest_raw_scrape.csv'

# --- GSheets Connection Details for GitHub Actions ---
GSPREAD_SERVICE_ACCOUNT_JSON = os.environ.get("GSPREAD_SERVICE_ACCOUNT")
GSPREAD_SHEET_NAME = "Micro Lead Custom Orders"
# ---------------------------------------------------


# --- TARGET MANAGEMENT ---

def get_scraping_targets():
    """Reads the order queue from GSheets and prepares a list of pending scrape targets."""
    targets = []
    worksheet = None # Initialize worksheet object

    # 1. Add Default Target (Maintenance run - always added first)
    targets.append({
        'niche': config['SCRAPING_CONFIG']['PRIMARY_NICHE'],
        'city': config['SCRAPING_CONFIG']['PRIMARY_CITY'],
        'max_count': 50,
        'order_status_index': -1 
    })

    # 2. Read Custom Orders from GSheets
    if GSPREAD_SERVICE_ACCOUNT_JSON:
        try:
            # Authenticate using the secret
            service_account_json = json.loads(GSPREAD_SERVICE_ACCOUNT_JSON)
            gc = gspread.service_account_from_dict(service_account_json)
            worksheet = gc.open(GSPREAD_SHEET_NAME).sheet1
            
            # Get all data as a list of dictionaries (Pandas-compatible)
            # This data includes the header row, so the index starts at 0 for data rows
            df_orders = pd.DataFrame(worksheet.get_all_records())
            
            # Filter for PENDING orders only
            pending_orders = df_orders[df_orders['status'] == 'PENDING_SCRAPE']
            
            for index, row in pending_orders.iterrows():
                targets.append({
                    'niche': row['niche'],
                    'city': row['location'],
                    'max_count': row['max_count'],
                    # The index here is the Pandas DataFrame index
                    'order_status_index': index 
                })
            
            # Return targets, the full DataFrame, and the worksheet object
            return targets, df_orders, worksheet
        
        except Exception as e:
            print(f"FATAL: GSheets API Read Failed. Ensure key is valid and sheet is shared. Error: {e}")
            return targets, pd.DataFrame(), None
    
    return targets, pd.DataFrame(), None


def update_order_status(worksheet, df_orders, targets_to_update, status):
    """Updates the status of processed orders in the Google Sheet (CRITICAL)."""
    
    if worksheet is None or df_orders.empty:
        print("Warning: Skipping status update (No worksheet or empty orders).")
        return
        
    try:
        # Get the header row to find column index
        header = worksheet.row_values(1)
        status_col_index = header.index('status') + 1 # GSheets is 1-indexed

        for target in targets_to_update:
            # The row number is the Pandas index + 2 (1 for 1-based, 1 for header row)
            row_number = target['order_status_index'] + 2
            
            # Update the cell (row, column, value)
            worksheet.update_cell(row_number, status_col_index, status)
                
        print(f"Successfully updated {len(targets_to_update)} order statuses to {status} in Google Sheets.")
        
    except Exception as e:
        print(f"FATAL: GSheets status update failed: {e}")


# --- SCRAPING FUNCTION (Remains the same as the stable version) ---
def execute_scrape(target, scrape_count_offset):
    """MOCK: Generates data using the exact schema the Verifier expects."""
    niche = target['niche']
    city = target['city']
    max_count = target['max_count']
    
    seed = (hash(niche) + hash(city)) % 1000
    random.seed(seed)
    
    count_scraped = min(random.randint(max_count // 5, max_count // 2), 50)
    
    print(f"--- SCRAPING TARGET: {niche} in {city} (Scraping {count_scraped} leads) ---")
    
    scraped_leads = []
    for i in range(count_scraped): 
        
        # CRITICAL FIX: Use the exact capitalized column names
        scraped_leads.append({
            'Business Name': f"{niche.title().split()[0]} Lead {scrape_count_offset + i}",
            'Niche': niche,                        
            'City': city,                   
            'Phone': f"+1 {random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",     
            'Email': f"test_lead_{scrape_count_offset + i}@{city.lower().replace(' ', '')}.com", 
            
            # ENRICHMENT COLUMNS (MOCKING them here)
            'Lead Score': random.randint(65, 95),
            'Reason to Contact': random.choice(['New Business in Your Area', 'No Website', 'High Conversion Potential']),
            'Attribute': random.choice(['New Businesses', 'No Website', 'High Conversion']), 
            
            'source_url': f"http://source.com/lead_{scrape_count_offset + i}",
            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    return pd.DataFrame(scraped_leads)


# --------------------------------------------------
# MAIN WORKFLOW EXECUTION
# --------------------------------------------------

if __name__ == "__main__":
    
    all_raw_data = []
    processed_order_indices = []
    scrape_count_offset = 0 
    
    # NEW: Now retrieves the worksheet object as well
    targets, df_orders, worksheet = get_scraping_targets() 
    
    if not targets:
        print("No scraping targets found. Exiting.")
        exit(0)

    print(f"Pipeline running for {len(targets)} target groups.")

    # 1. Execute all scraping jobs
    for target in targets:
        df_scrape_output = execute_scrape(target, scrape_count_offset) 
        
        all_raw_data.append(df_scrape_output)
        scrape_count_offset += len(df_scrape_output)
        
        # Track which custom orders successfully ran
        if target['order_status_index'] != -1:
            processed_order_indices.append(target) # Store the entire target dict

    # 2. Combine all raw data
    if all_raw_data:
        df_combined_raw = pd.concat(all_raw_data, ignore_index=True)
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(RAW_OUTPUT_PATH), exist_ok=True)
        
        # Save combined raw data (ready for clean_verify.py)
        df_combined_raw.to_csv(RAW_OUTPUT_PATH, index=False)
        print(f"Scrape phase complete. Total raw leads saved: {len(df_combined_raw)}")
        
        # 3. Update the status of the orders that were just scraped in Google Sheets
        if processed_order_indices:
            update_order_status(worksheet, df_orders, processed_order_indices, 'SCRAPE_COMPLETE')
            
    else:
        print("No data was generated by the scraper targets.")
        
    exit(0)
