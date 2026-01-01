import pandas as pd
import time
import random
import yaml
import os
from datetime import datetime

# --- CONFIGURATION & PATHS ---
try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config/config.yaml not found.")
    exit(1)

RAW_OUTPUT_PATH = 'data/raw/latest_raw_scrape.csv'
ORDER_QUEUE_PATH = 'data/requests/order_queue.csv'

# --- TARGET MANAGEMENT ---

def get_scraping_targets():
    """Reads the order queue and prepares a list of pending scrape targets."""
    targets = []
    
    # 1. Add Default Target (Maintenance run)
    targets.append({
        'niche': config['SCRAPING_CONFIG']['PRIMARY_NICHE'],
        'city': config['SCRAPING_CONFIG']['PRIMARY_CITY'],
        'max_count': 50, # Arbitrary maintenance count
        'order_status_index': -1 
    })

    # 2. Read Custom Orders from the Dashboard (order_queue.csv)
    if os.path.exists(ORDER_QUEUE_PATH):
        try:
            df_orders = pd.read_csv(ORDER_QUEUE_PATH)
            
            # Filter for PENDING orders only
            pending_orders = df_orders[df_orders['status'] == 'PENDING_SCRAPE']
            
            for index, row in pending_orders.iterrows():
                targets.append({
                    'niche': row['niche'],
                    'city': row['location'],
                    'max_count': row['max_count'],
                    'order_status_index': index
                })
            
            return targets, df_orders 
        except Exception as e:
            print(f"Warning: Could not read order queue CSV: {e}")
            return targets, pd.DataFrame()
    
    return targets, pd.DataFrame()


def update_order_status(df_orders, index_list, status):
    """Updates the status of processed orders in the DataFrame."""
    if not df_orders.empty:
        for index in index_list:
            if index != -1: 
                df_orders.loc[index, 'status'] = status
        
        # Save the updated queue
        os.makedirs(os.path.dirname(ORDER_QUEUE_PATH), exist_ok=True)
        df_orders.to_csv(ORDER_QUEUE_PATH, index=False)
        print(f"Successfully updated {len(index_list)} order statuses to {status}.")


# --- SCRAPING FUNCTION ---

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
        
        # CRITICAL FIX: Use the exact capitalized column names and local variable 'niche'
        scraped_leads.append({
            'Business Name': f"{niche.title().split()[0]} Lead {scrape_count_offset + i}",
            'Niche': niche,                        
            'City': city,                   
            'Phone': f"+1 {random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",     
            'Email': f"test_lead_{scrape_count_offset + i}@{city.lower().replace(' ', '')}.com", 
            
            # ENRICHMENT COLUMNS (MOCKING them here)
            'Lead Score': random.randint(65, 95),
            'Reason to Contact': random.choice(['New Business in Your Area', 'No Website', 'High Conversion Potential']),
            'Attribute': random.choice(['New Businesses', 'No Website', 'High Conversion']), # Used for Hero Cards
            
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
    
    targets, df_orders = get_scraping_targets()
    
    if not targets:
        print("No scraping targets found. Exiting.")
        exit(0)

    print(f"Pipeline running for {len(targets)} target groups.")

    # 1. Execute all scraping jobs
    for target in targets:
        # FIX: Ensure we pass both arguments as required by the function signature
        df_scrape_output = execute_scrape(target, scrape_count_offset) 
        
        all_raw_data.append(df_scrape_output)
        scrape_count_offset += len(df_scrape_output)
        
        if target['order_status_index'] != -1:
            processed_order_indices.append(target['order_status_index'])

    # 2. Combine all raw data
    if all_raw_data:
        df_combined_raw = pd.concat(all_raw_data, ignore_index=True)
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(RAW_OUTPUT_PATH), exist_ok=True)
        
        # Save combined raw data (ready for clean_verify.py)
        df_combined_raw.to_csv(RAW_OUTPUT_PATH, index=False)
        print(f"Scrape phase complete. Total raw leads saved: {len(df_combined_raw)}")
        
        # 3. Update the status of the orders that were just scraped
        if processed_order_indices:
            update_order_status(df_orders, processed_order_indices, 'SCRAPE_COMPLETE')
            
    else:
        print("No data was generated by the scraper targets.")
        
    exit(0)
