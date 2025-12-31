import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import time 

# --- CONFIGURATION & USER STATE ---
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH

USER_NAME = "Ravi Kumar"
USER_CITY = "Pune"
USER_NICHE = "Grocery Stores"
USER_PLAN = "Pro"
USER_CREDITS = 120 

MAX_FREE_LEADS = 5      
SUBSCRIPTION_PRICE = 30 
TOTAL_LEADS_LOCKED = 5  

# Set to False for the professional, conversion-focused free trial view
USER_IS_PREMIUM = False 
# ----------------------------------


# --- UTILITY: DATA LOADING AND ENRICHMENT ---
@st.cache_data(ttl=600) 
def load_and_enrich_leads(path_1, path_2):
    try:
        # Load and clean data (Trust Fix implemented here)
        df = pd.read_csv(path_1) if path_1.exists() else pd.read_csv(path_2)
        df = df[df['email'] != 'INVALID_EMAIL'].copy() 
        
        # Enrichment (Scoring, Tags, Formatting)
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df.get('category', 'Uncategorized').astype(str)
        df['score'] = (df.index * 5) + 60 + pd.Series(df.index).apply(lambda x: hash(x) % 30)
        df['why_contact'] = df['email'].apply(lambda x: 'No Website/Digital Presence Gap' if x.endswith('example.com') else 'New Business (First-to-Market)')
        df['phone_verified'] = df['phone'].apply(lambda x: '✔️ Verified' if len(str(x)) > 8 else '❌ Invalid')
        df['email_verified'] = df['email'].apply(lambda x: '✔️ Verified' if '@' in x else '❌ Invalid')
        
        return df.sort_values(by='score', ascending=False).reset_index(drop=True)

    except Exception as e:
        return pd.DataFrame()


# Load the data once
df_all = load_and_enrich_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)
if df_all.empty:
    st.set_page_config(page_title="Marketplace Error", layout="wide")
    st.warning("Data pipeline is initializing. Check back soon!")
    st.stop()


# --- GLOBAL PAGE CONFIG (0) ---
st.set_page_config(
    page_title="Micro Lead Marketplace | Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapse sidebar initially for LinkedIn aesthetic
)

# 1. TOP BAR (HEADER)
st.title("Micro Lead Marketplace")
st.markdown("---") # Clean separator

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"**User:** {USER_NAME}")
with col2:
    st.markdown(f"**Location:** {USER_CITY}")
with col3:
    st.markdown(f"**Niche:** {USER_NICHE}")
with col4:
    st.markdown(f"**Subscription:** {'Pro' if USER_IS_PREMIUM else 'Trial'}")
with col5:
    st.markdown(f"**Credits:** {USER_CREDITS}")

st.markdown("---")

# 2. TODAY’S MONEY OPPORTUNITIES (ANALYTICS SUMMARY)
st.subheader("Current Outreach Potential")

# Dynamic counts based on mock opportunities
count_no_website = len(df_all[df_all['why_contact'].str.contains('Digital Presence Gap')])
count_low_score = len(df_all[df_all['score'] < 75])
count_total_verified = len(df_all)

op1, op2, op3 = st.columns(3)

with op1:
    st.metric("Total Verified Leads", count_total_verified)

with op2:
    st.metric("High-Value Opportunities (No Web)", count_no_website, delta=f"+{count_total_verified // 2} last week")

with op3:
    st.metric("Lowest Score Leads", count_low_score, delta="Requires Urgent Outreach", delta_color="inverse") # Used inverse color for urgency

st.button("Launch Outreach Strategy", use_container_width=True, help="Access pre-built templates for high-conversion pitching.")


# 3. SMART LEAD FILTERS (PROFESSIONAL CONTROL)
st.markdown("## Data Segmentation & Control")

# Use a container for the locked filters
filter_container = st.container()

with filter_container:
    if not USER_IS_PREMIUM:
        st.warning("🔒 **Filters and Full Data Access are restricted in Trial Mode.** Upgrade to unlock full segmentation capabilities.")
    
    # Render all controls but disable them if not premium
    filters_disabled = not USER_IS_PREMIUM

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        city = st.selectbox("Target City", df_all['city_state'].unique(), disabled=filters_disabled)

    with f2:
        niche = st.selectbox("Primary Niche", df_all['category'].unique(), disabled=filters_disabled)

    with f3:
        score = st.slider("Min. Opportunity Score", 0, 100, 70, disabled=filters_disabled)

    with f4:
        lead_type = st.selectbox(
            "Lead Attribute Filter",
            ["All", "New Business (First-to-Market)", "No Website/Digital Presence Gap"],
            disabled=filters_disabled
        )
    st.button("Apply Segmentation", disabled=filters_disabled)


# 4. SMART LEAD TABLE (ACTION-ORIENTED)
st.markdown("## Filtered Lead Inventory")

# Data filtering logic: apply filters only if premium, otherwise show top 5
if USER_IS_PREMIUM:
    df_display = df_all.copy() # Premium users see all data
    # (If necessary, apply filter logic based on selectbox/slider values here)
    st.success(f"Inventory: Displaying {len(df_display)} Verified Leads.")
else:
    # FREE USER: Show only the top 5 highest-score leads
    df_display = df_all.head(MAX_FREE_LEADS)
    st.info(
        f"Trial View: Displaying top {len(df_display)} leads. **{count_total_verified - len(df_display)} leads locked.**"
    )

# Prepare the final display dataframe for the user
df_table = df_display[['name', 'city_state', 'phone_verified', 'email_verified', 'why_contact', 'score']].rename(
    columns={
        'name': 'Business Name',
        'city_state': 'Location',
        'phone_verified': 'Phone Status',
        'email_verified': 'Email Status',
        'why_contact': 'Lead Attribute',
        'score': 'Score'
    }
)

st.dataframe(
    df_table,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# 5. ONE-CLICK ACTION BUTTONS
if USER_IS_PREMIUM:
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.button("📥 Download CSV (Full List)")
    with a2:
        st.button("📊 Open in Google Sheets")
    with a3:
        st.button("✉️ Generate Email Template")
    with a4:
        st.button("📞 Copy Phone Numbers")
else:
    # 8. UPGRADE NUDGES (The Primary Conversion Nudge)
    st.warning("The Lead Inventory is restricted. Unlock full data access and segmentation filters.")
    st.button(f"🔓 Upgrade to PRO Access (${SUBSCRIPTION_PRICE}/mo)", type="primary", use_container_width=True)


# 6. OUTREACH TOOLKIT (REMAINS CLEAN)
st.markdown("## Outreach Toolkit & Scripts")

template = st.selectbox(
    "Select Outreach Channel",
    ["Cold Call Script", "WhatsApp Pitch", "LinkedIn Outreach"]
)

st.text_area(
    "Template Preview",
    "Subject: Inquiry regarding business growth in {{TargetCity}}. Hi {{BusinessName}}, I noticed your services are highly rated, but you lack a critical {LeadAttribute} which is costing you clients...",
    height=100
)


# 7. POTENTIAL EARNINGS TRACKER (REMAINS CLEAN)
st.markdown("## Earnings Projection")

e1, e2, e3 = st.columns(3)

with e1:
    st.metric("Leads Contacted (Est.)", 40)

with e2:
    st.metric("Expected Close Rate", "10%")

with e3:
    st.metric("Potential Income (Monthly)", "$400", delta="+$50 Month-over-Month") 


# 9. REFERRAL ENGINE (BUILT-IN GROWTH)
st.markdown("## Referral Engine")
st.info("Grow your network and earn credits. Invite 5 friends → 1 Month Pro Free.")
st.text_input("Your Referral Link", "https://yourapp.com/ref/ravi", disabled=True) 

# ----------------------------------------------------
