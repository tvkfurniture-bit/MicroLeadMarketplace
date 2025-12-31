import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import numpy as np # For mock chart data generation

# --- CONFIGURATION & USER STATE ---
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH

USER_NAME = "Ravi Kumar"
USER_PLAN = "Trial"
TOTAL_LEADS_IN_SYSTEM = 1850 # Mock Total System Size
EXPECTED_CLOSE_RATE = "10%"

MAX_FREE_LEADS = 5      
SUBSCRIPTION_PRICE = 30 
USER_IS_PREMIUM = False 

# --- UTILITY: DATA LOADING AND ENRICHMENT ---
@st.cache_data(ttl=600) 
def load_and_enrich_leads(path_1, path_2):
    try:
        df = pd.read_csv(path_1) if path_1.exists() else pd.read_csv(path_2)
        df = df[df['email'] != 'INVALID_EMAIL'].copy() 
        
        # Enrichment & Scoring
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df.get('category', 'Uncategorized').astype(str)
        df['score'] = (df.index * 5) + 60 + pd.Series(df.index).apply(lambda x: hash(x) % 30)
        df['why_contact'] = df['email'].apply(lambda x: 'Digital Presence Gap' if x.endswith('example.com') else 'First-to-Market')
        df['phone_status'] = df['phone'].apply(lambda x: 'Verified')
        df['email_status'] = df['email'].apply(lambda x: 'Verified')
        
        return df.sort_values(by='score', ascending=False).reset_index(drop=True)

    except Exception as e:
        return pd.DataFrame()

df_all = load_and_enrich_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)

# Calculate System KPIs
if not df_all.empty:
    TOTAL_VERIFIED_LEADS = len(df_all)
    TOTAL_LOCKED_LEADS = TOTAL_VERIFIED_LEADS - MAX_FREE_LEADS
    VERIFICATION_RATE = f"{len(df_all) / (len(df_all) + 3) * 100:.1f}%" # Mock calculation
else:
    TOTAL_VERIFIED_LEADS = 0
    TOTAL_LOCKED_LEADS = 0
    VERIFICATION_RATE = "0%"

# --- GLOBAL PAGE CONFIG ---
st.set_page_config(
    page_title="Micro Lead Marketplace | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded" # Use expanded sidebar for SaaS look
)

# --- SIDEBAR (SaaS Navigation Look) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1200px-React-icon.svg.png", width=30) # Placeholder Logo
    st.title("PROSPEKTA") # Mock Tool Name

    st.markdown("---")
    
    st.markdown("### 📊 DASHBOARD")
    st.button("🏠 Overview", use_container_width=True)
    st.button("⚙️ Settings", use_container_width=True)
    st.button("🔔 Integrations", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 👤 ACCOUNT")
    st.button("Profile & Billing", use_container_width=True)
    st.button("Logout", use_container_width=True)
    
    st.markdown("---")
    st.caption("© Micro Lead Marketplace 2026")
    st.info(f"Current Plan: {USER_PLAN}")


# --- MAIN CONTENT AREA ---

# 1. TOP BAR (Welcome & Search)
col_head, col_search = st.columns([10, 2])
with col_head:
    st.header("Overview")
    st.subheader(f"Welcome back, {USER_NAME}")
with col_search:
    st.text_input("Search Leads", placeholder="Search...", label_visibility="collapsed")
    
st.markdown("---")

# 2 & 7. KPI CARDS (DENSITY & PROFESSIONALISM)
st.subheader("Key Performance Indicators")
kpi_cols = st.columns(6)

# KPI 1: Total Leads
kpi_cols[0].metric("Total Leads (Verified)", TOTAL_VERIFIED_LEADS, delta="+5 Month-over-Month", delta_color="normal")
# KPI 2: Verification Rate
kpi_cols[1].metric("Verification Rate", VERIFICATION_RATE, delta="-0.5%", delta_color="inverse")
# KPI 3: Outreach Potential Score (Mock)
kpi_cols[2].metric("Outreach Score", "84/100", delta="+2 pts")
# KPI 4: Expected Close Rate (Ravi's Goal)
kpi_cols[3].metric("Expected Close Rate", EXPECTED_CLOSE_RATE)
# KPI 5: Potential Monthly Income
kpi_cols[4].metric("Monthly Potential Income", "$400", delta="+$50", delta_color="normal")
# KPI 6: Credits/Budget
kpi_cols[5].metric("Credits/Budget Remaining", f"{USER_CREDITS}", delta="-10 Used Today", delta_color="inverse")


# 3. LEAD GENERATION TRENDS (SIMULATED CHART)
st.markdown("<br>", unsafe_allow_html=True) # Spacer
st.subheader("Lead Generation Trends (Last 12 Months)")

# Mock Data for Chart
chart_data = pd.DataFrame(
    np.random.randn(12, 3),
    columns=['Total Generated', 'Verified', 'Used']
)
chart_data.index = pd.to_datetime(pd.date_range('2024-01-01', periods=12, freq='M')).strftime('%Y-%m')

st.line_chart(chart_data)

st.markdown("---")

# 4. DATA SEGMENTATION & LEAD INVENTORY (FILTERS AND TABLE)
st.subheader("Data Segmentation & Inventory")

if not USER_IS_PREMIUM:
    st.warning("🔒 Filters and Full Inventory Access are restricted in Trial Mode.")

# Filter Controls (Disabled based on plan)
filter_cols = st.columns(4)
with filter_cols[0]:
    st.selectbox("City/Location", df_all['city_state'].unique(), disabled=not USER_IS_PREMIUM)
with filter_cols[1]:
    st.selectbox("Niche/Industry", df_all['category'].unique(), disabled=not USER_IS_PREMIUM)
with filter_cols[2]:
    st.slider("Min. Opportunity Score", 0, 100, 70, disabled=not USER_IS_PREMIUM)
with filter_cols[3]:
    st.selectbox("Lead Attribute", ["All", "Digital Presence Gap", "First-to-Market"], disabled=not USER_IS_PREMIUM)
    st.button("Apply Filter", disabled=not USER_IS_PREMIUM)

# Data Filtering for Display
if USER_IS_PREMIUM:
    df_display = df_all.copy() 
else:
    # FREE USER: Show only the top 5 cleanest leads
    df_display = df_all.head(MAX_FREE_LEADS)


# 4. SMART LEAD TABLE (ACTION-ORIENTED)
st.markdown(f"#### Filtered Leads ({len(df_display)} displayed)")

st.dataframe(
    df_display[['name', 'city_state', 'phone_status', 'email_status', 'why_contact', 'score']].rename(
        columns={
            'name': 'Business',
            'city_state': 'Location',
            'phone_status': 'Phone',
            'email_status': 'Email',
            'why_contact': 'Opportunity',
            'score': 'Score'
        }
    ),
    use_container_width=True,
    hide_index=True,
    # Use column configuration to enhance the professional look
    column_config={
        "Score": st.column_config.ProgressColumn("Score", format="%d", min_value=0, max_value=100)
    }
)


# 5. ONE-CLICK ACTION BUTTONS / 8. UPGRADE NUDGE
action_cols = st.columns(5)

if USER_IS_PREMIUM:
    with action_cols[0]: st.button("📥 Download CSV (Full List)")
    with action_cols[1]: st.button("📊 Open in Google Sheets")
    with action_cols[2]: st.button("✉️ Generate Email Template")
    with action_cols[3]: st.button("📞 Copy Phone Numbers")
else:
    # Upgrade Nudge (Centralized and prominent)
    with action_cols[0]:
        st.markdown("<br>", unsafe_allow_html=True)
    with action_cols[1]:
        st.markdown("<br>", unsafe_allow_html=True)
    with action_cols[2].container(border=True): # Use a container to make the upgrade card prominent
        st.markdown(f"**{TOTAL_LOCKED_LEADS} Leads Locked**")
        st.button(f"🔓 Upgrade to PRO Access (${SUBSCRIPTION_PRICE}/mo)", type="primary")


st.markdown("---")

# 6. OUTREACH TOOLKIT
st.subheader("Outreach Toolkit & Scripts")
toolkit_cols = st.columns([1, 2])

with toolkit_cols[0]:
    st.selectbox(
        "Select Outreach Channel",
        ["Cold Call Script", "WhatsApp Pitch", "LinkedIn Outreach"]
    )
    # 9. REFERRAL ENGINE
    st.markdown("##### Referral Engine")
    st.info("Invite 1 friend → Get 50 free leads.")

with toolkit_cols[1]:
    st.text_area(
        "Template Preview (Actionable)",
        "Subject: High-Value Partnership Opportunity in {{City}}. Hi {{BusinessName}}, We noticed a critical Digital Presence Gap (Score: {{Score}}) that is costing you clients...",
        height=150
    )
