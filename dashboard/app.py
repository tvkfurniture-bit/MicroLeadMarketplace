import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import time 

# --- CONFIGURATION & SUBSCRIPTION LOGIC ---

RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH
REQUEST_QUEUE_PATH = Path(__file__).parent.parent / 'data/requests/order_queue.csv'

# Ravi's Requirements from the story
MAX_FREE_LEADS = 10 
SUBSCRIPTION_PRICE = 30 # $30/month for Unlimited

# --- SIMULATED USER STATE ---
# In a true V2, these would come from your login database (e.g., Supabase)
USER_IS_PREMIUM = False # <-- CHANGE THIS TO TEST PREMIUM VIEW
USER_LEADS_USED_THIS_WEEK = 0 
# ------------------------------


# --- Utility Functions (Data Loading) ---

@st.cache_data(ttl=600) 
def load_leads(path_1, path_2):
    # (Existing dual-path loading logic)
    # ... (function body remains the same, assuming it returns df or empty df) ...
    # Simplified return for brevity, assuming your previous path logic works:
    try:
        if path_1.exists():
            df = pd.read_csv(path_1)
        elif path_2.exists():
            df = pd.read_csv(path_2)
        else:
            return pd.DataFrame()

        # Add necessary filtering columns
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df['category'].astype(str)
        return df
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        return pd.DataFrame()


# --- Main App Logic ---

st.set_page_config(page_title="Micro Lead Marketplace", layout="wide")
st.title("🥇 The Micro Lead Marketplace")
st.markdown("### Verified, Hyperlocal B2B Leads, Refreshed Weekly.")

# Load the entire dataset
df_all = load_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)


# --- 1. SUBSCRIPTION AND FREE TRIAL GATE ---
df_display = df_all.copy()

if not USER_IS_PREMIUM and not df_all.empty:
    
    # Apply the 10-lead limit for the Free Trial
    # Ravi only sees the first 10 leads, sorted by potential value/recency
    df_display = df_all.head(MAX_FREE_LEADS) 
    
    st.info(
        f"🆓 Free Trial Active: Displaying {len(df_display)} of {len(df_all)} verified leads. "
        f"**Upgrade to Premium ($30/mo) for UNLIMITED access.**"
    )

# --- SIDEBAR: ENHANCED FILTERING ---
with st.sidebar:
    st.header("1. Filter Available Leads")
    
    if not USER_IS_PREMIUM:
        st.error("Filtering is restricted in Free Trial.")
        df_filtered = df_display.copy() # Free users can only "filter" the 10 they see.
    else:
        # PREMIUM USER: Show full filtering capabilities
        st.success("PREMIUM Access: Unlimited Filtering.")
        
        selected_niche = st.multiselect(
            "Industry", options=df_all['category'].unique(), 
            default=df_all['category'].iloc[0] if not df_all.empty else []
        )
        selected_location = st.multiselect(
            "Location", options=df_all['city_state'].unique(),
            default=df_all['city_state'].iloc[0] if not df_all.empty else []
        )
        
        df_filtered = df_all[
            (df_all['category'].isin(selected_niche)) &
            (df_all['city_state'].isin(selected_location))
        ]

    st.markdown("---")
    # This section remains the hook for custom orders
    st.header("2. Order New Leads")
    st.markdown("*(Future Feature: Place custom, paid niche scrape orders)*")
    # (Optional: Include the form from V2.1 here, but make sure it requires PREMIUM access)


# --- MAIN DISPLAY: DATA TABLE ---
if not df_display.empty:
    
    # 50 leads available, but only 10 shown if free
    available_count = len(df_filtered) if USER_IS_PREMIUM else len(df_display) 

    st.subheader(f"Available Leads ({available_count} matching your filter)")
    
    # Dataframe display for Ravi: prioritized columns (Name, Location, Phone, Email)
    st.dataframe(
        df_display[['name', 'category', 'city_state', 'phone', 'email']], 
        use_container_width=True,
        column_order=('name', 'category', 'city_state', 'phone', 'email'),
        column_config={
            "city_state": st.column_config.TextColumn("Location"),
            "phone": st.column_config.TextColumn("Phone (Verified)"),
            "email": st.column_config.TextColumn("Email (Verified)"),
        }
    )

    # Download Button Logic: Only active for premium users
    if USER_IS_PREMIUM:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"💾 Download ALL {len(df_filtered)} Leads (Subscription)",
            data=csv_data,
            file_name=f'premium_leads_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            help="Download unlimited leads with your Premium subscription."
        )
    else:
        # FREE USER CTA
        st.button("🔒 Upgrade to Download Leads ($30/mo)", type="primary")
        
    st.info(f"Last updated: {df_all['scraped_date'].max()}")

else:
    st.warning("The lead pipeline is empty. Check back after the next automated scrape.")
