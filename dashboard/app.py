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

# SIMULATED USER STATE (Crucial for monetization hooks)
USER_NAME = "Ravi Kumar"
USER_CITY = "Pune"
USER_NICHE = "Grocery Stores"
USER_PLAN = "Pro"
USER_CREDITS = 120 

MAX_FREE_LEADS = 5      # Only 5 best leads visible for free users
TOTAL_LEADS_LOCKED = 5  # Example: 5 specific high-value leads locked behind paywall

# IMPORTANT: SET THIS TO FALSE FOR THE CONVERSION FUNNEL DEMO
USER_IS_PREMIUM = False 
# ----------------------------------


# --- UTILITY: DATA LOADING AND ENRICHMENT ---

@st.cache_data(ttl=600) 
def load_and_enrich_leads(path_1, path_2):
    try:
        df = pd.read_csv(path_1) if path_1.exists() else pd.read_csv(path_2)

        # 1. CORE TRUST FIX: Filter out junk leads (Hides "INVALID_EMAIL" for trust)
        df = df[df['email'] != 'INVALID_EMAIL'].copy() 

        # 2. Add Enrichment Columns (Crucial for Hero Section and Table)
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df.get('category', 'Uncategorized').astype(str)
        
        # 3. Simulated Lead Scoring and Opportunity Tagging (Psychological Hook)
        df['score'] = (df.index * 5) + 60 + pd.Series(df.index).apply(lambda x: hash(x) % 30) # Simulated dynamic score
        df['why_contact'] = df['email'].apply(
            lambda x: 'No Website' if x.endswith('example.com') else 'New Business' # Mock logic
        )
        
        # 4. Action Icons
        df['phone_verified'] = df['phone'].apply(lambda x: '✅' if len(str(x)) > 8 else '❌')
        df['email_verified'] = df['email'].apply(lambda x: '✅' if '@' in x else '❌')
        
        return df.sort_values(by='score', ascending=False).reset_index(drop=True)

    except Exception as e:
        # st.error(f"Data loading failed: {e}") 
        return pd.DataFrame()

# Load the data once
df_all = load_and_enrich_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)

# --- SIDEBAR (10) ---
with st.sidebar:
    st.header("⚙️ Account")
    st.button("Profile")
    st.button("Billing")
    st.button("Logout")
    st.markdown("---")
    st.caption("© 2026 Micro Lead Marketplace")


# --- GLOBAL PAGE LAYOUT ---
if df_all.empty:
    st.warning("Data pipeline is initializing. Check back soon!")
    st.stop()
    
# 1. TOP BAR (HEADER)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"### 👤 {USER_NAME}")
with col2:
    st.markdown(f"📍 **City:** {USER_CITY}")
with col3:
    st.markdown(f"🎯 **Niche:** {USER_NICHE}")
with col4:
    st.markdown(f"💳 **Plan:** {'Pro' if USER_IS_PREMIUM else 'Trial'}")
with col5:
    st.markdown(f"🔢 **Credits:** {USER_CREDITS}")

# 2. TODAY’S MONEY OPPORTUNITIES (HERO SECTION)
st.markdown("---")
st.markdown("## 🔥 Today’s Best Money Opportunities")

# Dynamic counts based on mock opportunities
count_no_website = len(df_all[df_all['why_contact'] == 'No Website'])
count_poor_reviews = len(df_all[df_all['score'] < 75])
count_new_businesses = len(df_all[df_all['why_contact'] == 'New Business'])

op1, op2, op3 = st.columns(3)

with op1:
    st.success(f"🆕 {count_no_website} Leads with No Website\n\n_High-Value Offer_")

with op2:
    st.warning(f"📉 {count_poor_reviews} Leads with Low Score\n\n_Easy Pitch_")

with op3:
    st.info(f"📍 {count_new_businesses} New Businesses Today\n\n_First-to-Market_")

st.button("🚀 Start Outreach Now", use_container_width=True, type="primary")


# 3. SMART LEAD FILTERS (EARNINGS-FOCUSED)
st.markdown("## 🎯 Filter Leads That Make Money")

# Use st.form to capture filter state cleanly
with st.form("lead_filters"):
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        city = st.selectbox("City", df_all['city_state'].unique(), disabled=not USER_IS_PREMIUM)

    with f2:
        niche = st.selectbox("Niche", df_all['category'].unique(), disabled=not USER_IS_PREMIUM)

    with f3:
        score = st.slider("Min Lead Score", 0, 100, 70, disabled=not USER_IS_PREMIUM)

    with f4:
        lead_type = st.selectbox(
            "Opportunity Type",
            ["All", "New Business", "No Website", "Low Score"],
            disabled=not USER_IS_PREMIUM
        )
    
    # Apply button (Hidden/inactive for free users)
    st.form_submit_button("Apply Filters", disabled=not USER_IS_PREMIUM)


# 4. SMART LEAD TABLE (ACTION-ORIENTED)
st.markdown("## 📋 High Probability Leads")

# Data filtering logic
df_filtered = df_all.copy() # Start with all clean data

if USER_IS_PREMIUM:
    # APPLY FILTERS based on user choices
    df_filtered = df_filtered[df_filtered['score'] >= score]
    if lead_type != "All":
        df_filtered = df_filtered[df_filtered['why_contact'].str.contains(lead_type.replace('Low Score', 'score'))] # Simplified logic
else:
    # FREE USER: Show only the top 5 highest-score leads
    df_filtered = df_all.head(MAX_FREE_LEADS)


# Prepare the final display dataframe for the user
df_display = df_filtered[['name', 'phone_verified', 'email_verified', 'why_contact', 'score']].rename(
    columns={
        'name': 'Business',
        'phone_verified': 'Phone',
        'email_verified': 'Email',
        'why_contact': 'Why Contact',
        'score': 'Score'
    }
)

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)


# 5. ONE-CLICK ACTION BUTTONS
a1, a2, a3, a4 = st.columns(4)

with a1:
    st.button("📥 Download CSV", disabled=not USER_IS_PREMIUM)

with a2:
    st.button("📊 Open in Google Sheets", disabled=not USER_IS_PREMIUM)

with a3:
    st.button("✉️ Email Template", disabled=not USER_IS_PREMIUM)

with a4:
    st.button("📞 Copy Phone Numbers", disabled=not USER_IS_PREMIUM)


# 6. OUTREACH TOOLKIT (RIGHT SIDE PANEL)
st.markdown("## 🧰 Outreach Toolkit")

template = st.selectbox(
    "Choose Template",
    ["Cold Call Script", "WhatsApp Pitch", "Email Outreach"]
)

st.text_area(
    "Template Preview",
    "Hi {{BusinessName}}, I noticed you don’t have a website. We can help you capture clients who are searching for {{Niche}} services. Click to connect...",
    height=100
)


# 7. POTENTIAL EARNINGS TRACKER (PSYCHOLOGICAL HOOK)
st.markdown("## 💰 Potential Earnings")
# These are simulated numbers based on Ravi's profile
e1, e2, e3 = st.columns(3)

with e1:
    st.metric("Leads Contacted (Est.)", 40)

with e2:
    st.metric("Expected Close Rate", "10%")

with e3:
    st.metric("Potential Income (Monthly)", "$400", delta="+$50 from last month") # Added delta for growth hook


# 8. UPGRADE NUDGES (NON-INTRUSIVE)
if not USER_IS_PREMIUM:
    st.warning(f"🔒 {TOTAL_LEADS_LOCKED} High-Probability Leads Locked (Including Pune & Mumbai)")
    st.button("🔓 Upgrade to Unlock Premium Leads", type="primary", use_container_width=True)

# 9. REFERRAL ENGINE (BUILT-IN GROWTH)
st.markdown("## 🎁 Earn Free Leads")

st.info(
    "Invite 1 friend → Get 50 free leads\n\n"
    "Invite 5 friends → 1 Month Pro Free"
)

st.text_input("Your Referral Link", "https://yourapp.com/ref/ravi", disabled=True) # Disabled link for MVP
