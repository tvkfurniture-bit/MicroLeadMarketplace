import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# --- Configuration (Keep your robust paths) ---
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH
REQUEST_QUEUE_PATH = Path(__file__).parent.parent / 'data/requests/order_queue.csv'

# Assume AUTH succeeded for demonstration purposes (replace with your actual auth check)
ACCESS_TOKEN = "HVACLeads2026Q1" 
st.session_state['authenticated'] = True # <--- TEMP: SET TO TRUE FOR DEMO

# --- Utility Functions ---
@st.cache_data(ttl=600) 
def load_leads(path_1, path_2):
    # (Existing dual-path loading logic goes here)
    if path_1.exists():
        return pd.read_csv(path_1)
    elif path_2.exists():
        return pd.read_csv(path_2)
    else:
        st.error(f"Error: Lead data file not found at checked locations.")
        return pd.DataFrame()

# --- NEW: Function to save new lead requests ---
def save_lead_request(niche, location, max_count):
    new_request = pd.DataFrame({
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'niche': [niche],
        'location': [location],
        'max_count': [max_count],
        'user_id': ['Ravi_example'], # Link this to your authentication system later
        'status': ['PENDING_SCRAPE']
    })
    
    # Check if file exists, if so, append; otherwise, create new file
    if REQUEST_QUEUE_PATH.exists():
        new_request.to_csv(REQUEST_QUEUE_PATH, mode='a', header=False, index=False)
    else:
        # Ensure 'data/requests' exists if doing this manually
        os.makedirs(REQUEST_QUEUE_PATH.parent, exist_ok=True) 
        new_request.to_csv(REQUEST_QUEUE_PATH, index=False)
        
    return True
    
# --- Main App Logic ---

# Assuming Authentication has passed (if using the full auth block from the last response)
st.title("🥇 The Micro Lead Marketplace")
st.markdown("### Verified, hyperlocal B2B leads, refreshed weekly.")

df = load_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)

if not df.empty:
    
    # --- Data Pre-processing for Filtering ---
    # Temporarily extract City/Location for filtering (V3: this should be a clean column)
    df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
    df['category'] = df['category'].astype(str)

    # --- SIDEBAR: ENHANCED FILTERING ---
    st.sidebar.header("1. Filter Existing Leads")

    # 1. Niche Filter (Existing)
    unique_niches = df['category'].unique()
    selected_niche = st.sidebar.multiselect(
        "Select Industry Niche",
        options=unique_niches,
        default=df['category'].iloc[0] if len(unique_niches) > 0 else []
    )
    
    # 2. Location Filter (New)
    unique_locations = df['city_state'].unique()
    selected_location = st.sidebar.multiselect(
        "Select Location",
        options=unique_locations,
        default=unique_locations[0] if len(unique_locations) > 0 else []
    )
    
    # Apply Filters
    df_filtered = df[
        (df['category'].isin(selected_niche)) &
        (df['city_state'].isin(selected_location))
    ]

    # --- SIDEBAR: NEW LEAD ORDER FORM ---
    st.sidebar.markdown("---")
    st.sidebar.header("2. Order New Leads (Premium)")
    st.sidebar.markdown("*Don't see your niche? Place a custom order.*")

    with st.sidebar.form("new_lead_order"):
        niche_input = st.text_input("Industry Keyword (e.g., Grocery Stores)")
        location_input = st.text_input("City, Country (e.g., Pune, India)")
        max_leads_input = st.slider("Max Leads Desired", min_value=50, max_value=5000, step=50, value=500)
        
        submitted = st.form_submit_button("Place Order ($50)")
        
        if submitted:
            if niche_input and location_input:
                # Store the request for the GitHub Action to process later
                if save_lead_request(niche_input, location_input, max_leads_input):
                    st.success(f"Order for {niche_input} in {location_input} submitted! Leads will be available in the next batch (approx 24-48 hours).")
                else:
                    st.error("Error saving request.")
            else:
                st.error("Please fill in both Industry and Location.")


    # --- MAIN DISPLAY AREA ---
    st.subheader(f"Available Leads ({len(df_filtered)} matching your filter)")
    st.dataframe(df_filtered[['name', 'category', 'city_state', 'phone', 'email', 'source_url']], use_container_width=True)

    # Download Button 
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download All Filtered Leads (CSV)",
        data=csv_data,
        file_name='micro_leads_verified.csv',
        mime='text/csv',
        help="Access to this download requires a valid subscription."
    )
    
    st.info(f"Last updated: {df['scraped_date'].max()}")

else:
    st.warning("The lead pipeline is running or the first data pull is pending. Check back soon!")
