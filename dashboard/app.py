import streamlit as st
import pandas as pd
import os

# --- Configuration ---
LEAD_FILE_PATH = 'data/verified/verified_leads.csv'

# Set up page config
st.set_page_config(
    page_title="Micro Lead Marketplace",
    layout="wide"
)

# Use Streamlit's caching feature for fast performance
# It automatically re-runs if the underlying CSV file changes
@st.cache_data(ttl=600) 
def load_leads(path):
    """Load the verified leads CSV file."""
    if not os.path.exists(path):
        st.error("Lead data file not found. Pipeline may not have run yet.")
        return pd.DataFrame()
    return pd.read_csv(path)

# --- Monetization MOCK (V1) ---
# In V2, this checks a real user database (Supabase/Auth0)
def check_subscription_status(user_id):
    # MVP: Assume user is subscribed if they successfully logged in
    return True # Replace with real subscription check

# --- Dashboard UI ---
st.title("🥇 The Micro Lead Marketplace")
st.markdown("### Verified, hyperlocal B2B leads, refreshed weekly.")

df = load_leads(LEAD_FILE_PATH)

if not df.empty:
    st.sidebar.header("Filter Leads (Premium Feature)")

    # Filter 1: Niche
    unique_niches = df['category'].unique()
    selected_niche = st.sidebar.multiselect(
        "Select Industry Niche",
        options=unique_niches,
        default=unique_niches[0] if len(unique_niches) > 0 else []
    )
    
    df_filtered = df[df['category'].isin(selected_niche)]

    # Filter 2: Location (Add a location column and filter here in V2)
    # st.sidebar.text("Location filter coming soon!")
    
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
