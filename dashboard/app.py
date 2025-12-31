import streamlit as st
import pandas as pd
import os
# >>> ADD PATHLIB IMPORT FOR ROBUST FILE PATHS
from pathlib import Path

# --- Configuration ---

# 1. Define the relative path to the file
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'

# 2. Construct the ABSOLUTE path relative to the app.py script's location.
# Path(__file__).parent is the 'dashboard' directory.
# .parent again moves up to the project root 'MicroLeadMarketplace'.
LEAD_FILE_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH

# Set up page config
st.set_page_config(
    page_title="Micro Lead Marketplace",
    layout="wide"
)

# Use Streamlit's caching feature for fast performance
# Note: We now pass the Path object, not just a string
@st.cache_data(ttl=600) 
def load_leads(path_object):
    """Load the verified leads CSV file using the robust Path object."""
    
    # Check if the Path object exists (more reliable check)
    if not path_object.exists():
        st.error(f"Error: Lead data file not found at {path_object}. Please ensure the GitHub Action ran successfully.")
        return pd.DataFrame()
    
    # Read the CSV file
    return pd.read_csv(path_object)

# --- Dashboard UI ---
st.title("🥇 The Micro Lead Marketplace")
st.markdown("### Verified, hyperlocal B2B leads, refreshed weekly.")

# >>> PASS THE ROBUST PATH OBJECT TO THE LOADER
df = load_leads(LEAD_FILE_PATH)

if not df.empty:
    st.sidebar.header("Filter Leads (Premium Feature)")

    # Filter 1: Niche
    # Ensure all category names are treated as strings to avoid filtering errors
    df['category'] = df['category'].astype(str)
    unique_niches = df['category'].unique()
    
    # Handle the case where the first category might be 'nan' if data is slightly messy
    default_niche = unique_niches[0] if len(unique_niches) > 0 and pd.notna(unique_niches[0]) else []

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
    st.warning("The lead pipeline is running or the first data pull is pending. Check back soon!")
