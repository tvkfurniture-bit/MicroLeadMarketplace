import streamlit as st
import pandas as pd
import os
from pathlib import Path

# --- Configuration ---
# 1. Define the relative path to the file
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'

# 2. Try 1: Robust Pathlib relative to the script location (The correct standard way)
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH

# 3. Try 2: Absolute Path (The Streamlit deployment fail-safe)
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH

# --- NEW: AUTH CONFIG ---
# This is the key that paying users buy. (Must be updated manually/via secret later)
ACCESS_TOKEN = "HVACLeads2026Q1" 
# -------------------------


# Set up page config
st.set_page_config(
    page_title="Micro Lead Marketplace",
    layout="wide"
)

# Use Streamlit's caching feature for fast performance
@st.cache_data(ttl=600) 
def load_leads(path_1, path_2):
    """Loads the CSV, checking the most likely paths in the Streamlit environment."""
    
    # Check 1: Try the Pathlib relative path
    if path_1.exists():
        st.success(f"Loaded data successfully from standard path: {path_1}")
        return pd.read_csv(path_1)
    
    # Check 2: Try the hardcoded Streamlit absolute path (/app)
    elif path_2.exists():
        st.success(f"Loaded data successfully from Streamlit root path: {path_2}")
        return pd.read_csv(path_2)

    # If both fail, display error
    else:
        st.error(
            f"Error: Lead data file not found at either location."
            f" (Checked: {path_1} and {path_2}). "
            f"Please confirm file existence in GitHub repo."
        )
        return pd.DataFrame()

# --- Dashboard UI ---
st.title("🥇 The Micro Lead Marketplace")

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- AUTHENTICATION GATE ---
if not st.session_state['authenticated']:
    st.header("🔑 Premium Access Required")
    st.markdown("Enter your Subscription Key to access the verified leads.")

    input_key = st.text_input("Subscription Key:", type="password")
    
    if st.button("Access Marketplace"):
        if input_key == ACCESS_TOKEN:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid key. Purchase a subscription to receive access.")
    
    # Marketing hook for free users
    st.info("💡 Start your freelancing today! Subscribe for less than $1 a day.")
    
# --- END AUTHENTICATION GATE ---

# --- PREMIUM CONTENT DISPLAY (Only runs if authenticated) ---
if st.session_state['authenticated']:
    st.markdown("### Verified, hyperlocal B2B leads, refreshed weekly.")

    # Load data only AFTER auth check passes
    df = load_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)

    if not df.empty:
        st.sidebar.header("Filter Leads (Premium Feature)")

        # Ensure all category names are treated as strings to avoid filtering errors
        df['category'] = df['category'].astype(str)
        unique_niches = df['category'].unique()
        
        # Handle initial default selection
        default_niche = [n for n in unique_niches if pd.notna(n)][0] if len(unique_niches) > 0 and pd.notna(unique_niches[0]) else []

        selected_niche = st.sidebar.multiselect(
            "Select Industry Niche",
            options=unique_niches,
            default=default_niche
        )
        
        df_filtered = df[df['category'].isin(selected_niche)]

        st.subheader(f"Available Leads ({len(df_filtered)} matching your filter)")

        # Display the data table
        st.dataframe(df_filtered, use_container_width=True)

        # Download Button (The core transaction point)
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
        st.warning("No verified leads found. Please check filters or wait for the next weekly update.")
