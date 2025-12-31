import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import time # Used for simulating payment delay

# --- Configuration (Keep your robust paths) ---
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH

# New Path for User Orders
REQUEST_QUEUE_PATH = Path(__file__).parent.parent / 'data/requests/order_queue.csv'

# Assume AUTH succeeded for demonstration (MUST BE REPLACED WITH REAL AUTH)
st.session_state['authenticated'] = True 
ORDER_PRICE = 50 


# --- Utility Functions (Path and Data Loading) ---

@st.cache_data(ttl=600) 
def load_leads(path_1, path_2):
    # (Existing dual-path loading logic goes here)
    if path_1.exists():
        df = pd.read_csv(path_1)
        # Ensure 'city_state' is generated for filtering
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df['category'].astype(str)
        return df
    elif path_2.exists():
        df = pd.read_csv(path_2)
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df['category'].astype(str)
        return df
    else:
        st.error(f"Error: Lead data file not found at checked locations.")
        return pd.DataFrame()

def save_lead_request(niche, location, max_count):
    # This function is called AFTER simulated payment
    new_request = pd.DataFrame({
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'niche': [niche],
        'location': [location],
        'max_count': [max_count],
        'user_id': ['Ravi_example'], 
        'status': ['PENDING_SCRAPE']
    })
    
    # Check if file exists, if so, append; otherwise, create new file
    if REQUEST_QUEUE_PATH.exists():
        new_request.to_csv(REQUEST_QUEUE_PATH, mode='a', header=False, index=False)
    else:
        os.makedirs(REQUEST_QUEUE_PATH.parent, exist_ok=True) 
        new_request.to_csv(REQUEST_QUEUE_PATH, index=False)
        
    return True

# --- Main App Logic ---

# Assuming Authentication check passed
st.set_page_config(page_title="Micro Lead Marketplace", layout="wide")

st.title("🥇 The Micro Lead Marketplace")
st.markdown("### Verified, Hyperlocal B2B Leads, Refreshed Weekly.")

# Load the data once
df = load_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)


# --- SIDEBAR: ENHANCED FILTERING & ORDER FORM ---
with st.sidebar:
    
    st.header("1. Filter Existing Leads")
    
    if not df.empty:
        # 1. Niche Filter 
        unique_niches = df['category'].unique()
        selected_niche = st.multiselect(
            "Select Industry Niche",
            options=unique_niches,
            default=df['category'].iloc[0] if len(unique_niches) > 0 else []
        )
        
        # 2. Location Filter 
        unique_locations = df['city_state'].unique()
        selected_location = st.multiselect(
            "Select Location",
            options=unique_locations,
            default=unique_locations[0] if len(unique_locations) > 0 else []
        )
        
        # Apply Filters
        df_filtered = df[
            (df['category'].isin(selected_niche)) &
            (df['city_state'].isin(selected_location))
        ]
    else:
        st.warning("No leads loaded yet.")
        df_filtered = pd.DataFrame()


    st.markdown("---")
    st.header("2. Order New Leads (Premium)")
    st.markdown("*(Pay $50 for a batch scrape targeting your specific criteria)*")

    # Use a container for the form
    with st.form("new_lead_order"):
        niche_input = st.text_input("Industry Keyword (e.g., Hair Salon)", help="The exact phrase the scraper will search for.")
        location_input = st.text_input("City, Country (e.g., Pune, India)", help="The physical location to target.")
        max_leads_input = st.slider("Max Leads Desired", min_value=50, max_value=5000, step=50, value=500)
        
        # Simulated Payment Button
        pay_button = st.form_submit_button(f"🔒 Place Order & Pay ${ORDER_PRICE}")
        
        if pay_button:
            if niche_input and location_input:
                
                # --- START SIMULATED PAYMENT LOGIC ---
                with st.spinner(f"Processing payment of ${ORDER_PRICE} securely..."):
                    time.sleep(2) # Simulate network delay
                
                # --- Assume payment succeeded ---
                
                # Save the validated request
                if save_lead_request(niche_input, location_input, max_leads_input):
                    st.success(
                        f"✅ Payment Confirmed! Order for '{niche_input} in {location_input}' submitted. "
                        f"Leads will be scraped and available in 24-48 hours. Thank you, Ravi!"
                    )
                    # Force a redraw of the form area
                    st.rerun() 
                else:
                    st.error("Error saving request to queue.")
                    
                # --- END SIMULATED PAYMENT LOGIC ---

            else:
                st.error("Please fill in both Industry Keyword and Location.")


# --- MAIN DISPLAY: DATA TABLE ---
if not df_filtered.empty:
    st.subheader(f"Available Leads ({len(df_filtered)} matching your filter)")
    
    # Optimized Data Display (Hiding internal scrape columns like index)
    st.dataframe(
        df_filtered[['name', 'category', 'city_state', 'phone', 'email', 'source_url']], 
        use_container_width=True,
        # Improve column names for user view
        column_order=('name', 'category', 'city_state', 'phone', 'email'),
        column_config={
            "city_state": st.column_config.TextColumn("Location"),
            "source_url": st.column_config.LinkColumn("Source"),
            "email": st.column_config.TextColumn("Email (Verified)")
        }
    )

    # Download Button 
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"💾 Download {len(df_filtered)} Filtered Leads (CSV)",
        data=csv_data,
        file_name=f'micro_leads_{niche_input.replace(" ", "_")}.csv',
        mime='text/csv',
        key='download_btn',
        help="Download is unlocked with a paid subscription."
    )
    
    st.info(f"Last updated: {df['scraped_date'].max()}")

else:
    # This handles the case where the data file is loaded, but filters are too strict
    st.warning("No leads match your current filter criteria. Try broadening your selection or placing a New Lead Order above.")
