import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import time 

# --- CONFIGURATION & SUBSCRIPTION LOGIC ---

RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
# Using Pathlib and Absolute paths as established
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH

# Ravi's Requirements from the story
MAX_FREE_LEADS = 5 # Reduced to 5 to increase scarcity!
SUBSCRIPTION_PRICE = 10 

# --- SIMULATED USER STATE ---
USER_IS_PREMIUM = False # <-- Defaulting to non-paid user for conversion funnel demo
# ------------------------------


# --- Utility Functions (Data Loading) ---
@st.cache_data(ttl=600) 
def load_leads(path_1, path_2):
    # (Data loading logic remains the same)
    try:
        # Load data using the successful path logic
        df = pd.read_csv(path_1) if path_1.exists() else pd.read_csv(path_2)

        # 1. CORE TRUST FIX: FILTER OUT ALL VISIBLY INVALID LEADS (Hides INVALID_EMAIL)
        df = df[df['email'] != 'INVALID_EMAIL'].copy()

        # Add necessary filtering columns
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df.get('category', 'Uncategorized').astype(str) # Handle case where category might be missing
        df['is_verified'] = df['email'].apply(lambda x: 'Verified' if '@' in x else 'Unverified')

        return df
    except Exception as e:
        # st.error(f"Data loading failed: {e}") # Hide technical errors from users
        return pd.DataFrame()


# --- Main App Logic ---

st.set_page_config(page_title="Micro Lead Marketplace", layout="wide")
st.title("🥇 The Micro Lead Marketplace")
st.markdown("### Verified, Hyperlocal B2B Leads, Refreshed Weekly.")

# Load the entire dataset (which is now clean of visible junk)
df_all = load_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)


# --- SIDEBAR: TEMPTATION FILTERING ---
with st.sidebar:
    st.header("1. Filter Available Leads")
    
    # We always render the UI, but disable the controls if the user is Free
    
    # Use st.form and st.form_submit_button to structure the disabled filters cleanly
    with st.container():
        st.markdown(f"**Status:** {'✅ Premium' if USER_IS_PREMIUM else '🔓 Free Trial'}")
        
        # Display the power features they are missing
        st.selectbox(
            "Select Industry Niche",
            options=df_all['category'].unique(),
            disabled=not USER_IS_PREMIUM,
            index=0
        )
        st.selectbox(
            "Select Location",
            options=df_all['city_state'].unique(),
            disabled=not USER_IS_PREMIUM,
            index=0
        )
        
        # Display the locked download option clearly
        if not USER_IS_PREMIUM:
            st.error("Filtering and bulk download are premium features.")

    st.markdown("---")
    st.header("2. Subscribe Now")
    st.markdown(f"**Get UNLIMITED filtering and bulk downloads for just ${SUBSCRIPTION_PRICE}/mo.**")
    
    # BIG RED CTA BUTTON (Link to your payment system)
    st.button(f"🚀 Unlock PREMIUM Access (${SUBSCRIPTION_PRICE}/mo)", type="primary")
    st.markdown("*(Clicking this will redirect to a payment link)*")

# --- MAIN DISPLAY: DATA TABLE ---

if not df_all.empty:
    
    # DETERMINE DATA TO DISPLAY
    if USER_IS_PREMIUM:
        df_display = df_all.copy()
        st.success(f"✅ PREMIUM ACCESS: Displaying ALL {len(df_display)} Verified Leads.")
    else:
        # FREE TRIAL: Show only the top 5 cleanest leads
        df_display = df_all.head(MAX_FREE_LEADS)
        st.info(
            f"🆓 Free Trial Active: Displaying {len(df_display)} of {len(df_all)} verified leads. "
            f"**Upgrade to Premium for UNLIMITED access.**"
        )
        
    st.subheader(f"Leads Matching Your Needs ({len(df_display)})")
    
    # Display the clean leads
    st.dataframe(
        df_display[['name', 'category', 'city_state', 'phone', 'email']], 
        use_container_width=True,
        # Define columns clearly to show verification
        column_config={
            "city_state": st.column_config.TextColumn("Location"),
            "phone": st.column_config.TextColumn("Phone (Verified)"),
            "email": st.column_config.TextColumn("Email (Verified)"),
        }
    )

    # --- DOWNLOAD BUTTON LOGIC (Locked) ---
    if USER_IS_PREMIUM:
        # Only show download button if paid
        csv_data = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"💾 Download ALL {len(df_display)} Leads (Subscription)",
            data=csv_data,
            file_name=f'premium_leads_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )
    else:
        # Show a disabled button for temptation
        st.button("🔒 Download Leads (Requires Upgrade)", disabled=True)
        
    st.info(f"Last updated: {df_all['scraped_date'].max()}")

else:
    st.warning("The lead pipeline is empty. Check back after the next automated scrape.")
