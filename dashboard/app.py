import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime

# --------------------------------------------------
# CONFIGURATION & FILE PATH SETUP
# --------------------------------------------------
PREMIUM_ACCESS_KEY = "30DAYPRO" 
TRIAL_KEY = "TRIAL-ACCESS-12345" 
TRIAL_LEAD_LIMIT = 5 
SUBSCRIPTION_PRICE = 30
COLOR_RED_CTA = "#f87171" 
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"

# --- EXTERNAL URLS (Mockup) ---
PAYPAL_TRIAL_LINK = "https://www.paypal.com/instant-key-checkout-0dollar" 
EXTERNAL_UPGRADE_URL = "https://yourstripe.com/checkout/premium" 
EXTERNAL_REFERRAL_URL = "https://yourapp.com/ref/ravi" 

# --- FILE PATH SETUP (Connects to the GitHub Action output) ---
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH

# --------------------------------------------------
# SESSION STATE AND AUTH FUNCTIONS
# --------------------------------------------------

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'is_premium' not in st.session_state: st.session_state['is_premium'] = False
if 'payment_initiated' not in st.session_state: st.session_state['payment_initiated'] = False 
if 'user' not in st.session_state:
    st.session_state['user'] = {"name": "Trial User", "city": "N/A", "niche": "All", "plan": "Trial", "credits": 0}

# --- AUTH FUNCTIONS ---
def login_successful(key):
    if key == PREMIUM_ACCESS_KEY:
        st.session_state['logged_in'] = True
        st.session_state['is_premium'] = True
        st.session_state['user'] = {"name": "Ravi Kumar", "city": "Pune, India", "niche": "Grocery Stores", "plan": "Pro Plan", "credits": 85}
        st.session_state['filter_city'] = 'All'
        st.session_state['filter_niche'] = 'All'
        st.session_state['filter_score'] = 0
        st.session_state['filter_reason'] = 'All'
        st.rerun() 
        return True
    elif key == TRIAL_KEY:
        st.session_state['logged_in'] = True
        st.session_state['is_premium'] = False
        st.session_state['user'] = {"name": "New Trialist", "city": "Pune, India", "niche": "Grocery Stores", "plan": "Trial", "credits": 10}
        st.session_state['filter_city'] = 'Pune, India'
        st.session_state['filter_niche'] = 'Grocery Stores'
        st.session_state['filter_score'] = 70
        st.session_state['filter_reason'] = 'All'
        st.rerun() 
        return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['is_premium'] = False
    st.session_state['user'] = {"name": "Trial User", "city": "N/A", "niche": "All", "plan": "Trial", "credits": 0}
    st.session_state['payment_initiated'] = False
    st.rerun()

def go_to_url(url):
    """Function to inject JavaScript for external redirect."""
    st.markdown(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)


# --------------------------------------------------
# DATA LOADING AND HELPER FUNCTIONS
# --------------------------------------------------

def mask_email(email):
    if '@' in email and len(email.split('@')[0]) > 4:
        username, domain = email.split('@')
        return f"{username[:2]}****@{domain}"
    return email

def mask_phone(phone):
    if len(phone) > 8:
        return f"{phone[:8]}***-{phone[-4:]}"
    return phone

def render_hero_card(col, title, deal, count, color):
    with col.container(border=True, height=140):
        st.markdown(
            f'<div style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 14px;">{title}</div>', 
            unsafe_allow_html=True
        )
        st.markdown(f"**{deal}**", unsafe_allow_html=True)
        st.markdown(f"**{count}** Leads Available", help="Count of leads available for this segment.")


@st.cache_data(ttl=600)
def load_live_data():
    """Reads CSV from the pipeline and adds enrichment columns required by the UI."""
    
    if not PATHLIB_PATH.exists():
        st.warning(f"Waiting for first pipeline run. No data found at: {PATHLIB_PATH}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(PATHLIB_PATH)
        if df.empty:
            return pd.DataFrame()

        # --- ENRICHMENT LOGIC (Adds UI-required columns not in the raw CSV) ---
        
        # Rename columns from scraper output to UI expectations
        # Assumes scraper outputs: name, phone, email, category, address
        df.rename(columns={'name': 'Business Name', 'phone': 'Phone', 'email': 'Email', 'category': 'Niche'}, inplace=True)
        
        # Create UI-dependent columns (MOCK LOGIC)
        df['City'] = df['address'].apply(lambda x: x.split(',')[-2].strip() if x else 'N/A')
        df['Reason to Contact'] = np.random.choice(['No Website', 'New Business in Your Area', 'High Conversion Potential'], size=len(df))
        df['Attribute'] = df['Reason to Contact'].apply(lambda x: 'No Website' if 'Website' in x else 'New Businesses')

        df['Lead Score'] = np.random.randint(65, 95, size=len(df))
        df['Potential Deal'] = np.random.randint(300, 1500, size=len(df))
        
        # Apply Masking 
        is_premium = st.session_state.get('is_premium', False)
        df['Phone'] = df.apply(lambda row: row['Phone'] if is_premium else mask_phone(row['Phone']), axis=1)
        df['Email'] = df.apply(lambda row: row['Email'] if is_premium else mask_email(row['Email']), axis=1)
        
        return df.sort_values(by='Lead Score', ascending=False).reset_index(drop=True)

    except Exception as e:
        st.error(f"Error reading or processing live data: {e}")
        return pd.DataFrame()


# --------------------------------------------------
# GLOBAL DATA LOAD (This runs once when the script starts)
# --------------------------------------------------
df_raw = load_live_data() 

# Calculate KPIs from the live data
leads_new_biz_count = len(df_raw[df_raw['Attribute'] == 'New Businesses']) if not df_raw.empty else 0
leads_no_web_count = len(df_raw[df_raw['Attribute'] == 'No Website']) if not df_raw.empty else 0
leads_high_conv_count = len(df_raw[df_raw['Attribute'] == 'High Conversion']) if not df_raw.empty else 0


# --------------------------------------------------
# GLOBAL CSS INJECTION
# --------------------------------------------------
st.markdown(f"""
<style>
/* Adjust spacing for density */
.stApp {{ padding-top: 20px !important; padding-right: 30px !important; padding-left: 30px !important; }}
div[data-testid="stVerticalBlock"] > div:first-child {{ padding-top: 0 !important; }}
.st-emotion-cache-1mnrbfp {{ visibility: hidden !important; }}

/* Fix Primary Button Color to Red CTA */
.stButton>button[kind="primary"] {{
    background-color: {COLOR_RED_CTA} !important;
    color: white !important;
    border: none !important;
}}
/* Fix Header Alignment */
.header-buttons-container {{ display: flex; align-items: center; height: 100%; }}

/* Fix Title Font Size */
h1.st-emotion-cache-18nn76w {{ font-size: 24px !important; }}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Micro Lead Marketplace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# --- AUTHENTICATION GATE ---
# --------------------------------------------------
if not st.session_state['logged_in']:
    st.title("Micro Lead Marketplace Access")
    st.subheader("Start Your Free Trial — (Zero Dollar Purchase)")
    
    auth_cols = st.columns([2, 1, 1])
    
    if not st.session_state['payment_initiated']:
        st.warning("To ensure security, the Trial Key is delivered via email after a secure 0.00 transaction.")
        auth_cols[0].markdown(f"**1. Get Your Trial Key:** Click below to process your $0.00 secure key generation.", unsafe_allow_html=True)
        auth_cols[0].link_button("🔑 Process Trial Key via PayPal", url=PAYPAL_TRIAL_LINK, type="primary")

        if auth_cols[1].button("I Completed Payment", key="btn_check_payment"):
             st.session_state['payment_initiated'] = True
             st.rerun()

    if st.session_state['payment_initiated'] or not st.session_state['logged_in']:
        st.markdown("---")
        
        if st.session_state['payment_initiated'] and not st.session_state['logged_in']:
             st.success(f"Key has been generated and sent! Check your inbox for the key: **{TRIAL_KEY}**")
             st.warning("Please use the key above for immediate login (MOCK).")
        
        key_input = auth_cols[0].text_input("Enter Key Received in Email:", type="password", key="auth_key_input")
        
        if auth_cols[1].button("Login", key="btn_final_login", type="secondary"):
            if login_successful(key_input):
                pass
            else:
                st.error("Invalid key or key expired.")
                
    st.stop()


# --------------------------------------------------
# --- APPLICATION START: LOGGED IN USER VIEW ---
# --------------------------------------------------

# 1. TOP HEADER BAR
header_cols = st.columns([0.1, 7, 1, 1, 0.5]) 

with header_cols[0]: st.markdown("Ⓜ️") 
with header_cols[1]: # User Info Bar
    meta_cols = st.columns([2, 1.5, 2, 1.5])
    with meta_cols[0]: st.markdown(f"**Micro B2B Lead Marketplace**", unsafe_allow_html=True)
    with meta_cols[1]: st.caption(f"Welcome: {st.session_state['user']['name']}")
    with meta_cols[2]: st.caption(f"{st.session_state['user']['city']} | Niche: {st.session_state['user']['niche']}")
    with meta_cols[3]: st.caption(f"**{st.session_state['user']['plan']}** | Credits: {st.session_state['user']['credits']}")

# --- RIGHT BUTTONS ---
with header_cols[2]: 
    if st.button("Upgrade Plan", key="upgrade_top_bar"):
        go_to_url(EXTERNAL_UPGRADE_URL)

with header_cols[3]:
    if st.button("Refer & Earn", key="refer_top_bar", type="primary"):
        go_to_url(EXTERNAL_REFERRAL_URL)

with header_cols[4]:
    st.button("☰", use_container_width=True, key="menu_top_bar", on_click=logout) 

st.markdown("---")

# 2. TODAY'S OPPORTUNITIES (HERO CARDS)
st.markdown("## Today’s Best Money Opportunities")
main_content_cols = st.columns([9, 3])

# --- DYNAMIC FILTER STATE ---
if 'filter_city' not in st.session_state: st.session_state['filter_city'] = st.session_state['user']['city']
if 'filter_niche' not in st.session_state: st.session_state['filter_niche'] = st.session_state['user']['niche']
if 'filter_score' not in st.session_state: st.session_state['filter_score'] = 70
if 'filter_reason' not in st.session_state: st.session_state['filter_reason'] = 'All'


# --- DYNAMIC FILTERING LOGIC ---
df_current_view = df_raw.copy() 
is_premium = st.session_state['is_premium']

# APPLY FILTERS based on session state
if is_premium:
    if st.session_state['filter_city'] != 'All': 
        df_current_view = df_current_view[df_current_view['City'] == st.session_state['filter_city']]
    if st.session_state['filter_niche'] != 'All': 
        df_current_view = df_current_view[df_current_view['Niche'] == st.session_state['filter_niche']]
    if st.session_state['filter_score'] > 0: 
        df_current_view = df_current_view[df_current_view['Lead Score'] >= st.session_state['filter_score']]
    if st.session_state['filter_reason'] != 'All':
        df_current_view = df_current_view[df_current_view['Reason to Contact'].str.contains(st.session_state['filter_reason'], case=False, na=False)]
    
    total_leads_for_display = len(df_current_view)
    df_filtered_for_display = df_current_view
else:
    # Trial Logic: Enforce Ravi's default niche and limit leads
    df_current_view = df_current_view[df_current_view['City'].str.contains(st.session_state['user']['city'], case=False, na=False)]
    df_current_view = df_current_view[df_current_view['Niche'].str.contains(st.session_state['user']['niche'], case=False, na=False)]
    
    total_leads_for_display = len(df_current_view) 
    df_filtered_for_display = df_current_view.head(TRIAL_LEAD_LIMIT)


# --- LEFT COLUMN: HERO CARDS & TABLE ---
with main_content_cols[0]:
    
    hero_cols = st.columns(3)
    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", leads_new_biz_count, COLOR_BLUE)
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", leads_no_web_count, COLOR_GREEN)
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", leads_high_conv_count, COLOR_ORANGE)

    # 5. ACTION BAR 
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    
    if is_premium:
        with action_buttons[0]: st.button("📥 Download CSV", key="act_csv")
        with action_buttons[1]: st.button("📊 Open in Google Sheets", key="act_sheets")
        with action_buttons[2]: st.button("✉️ Send Email", key="act_email")
        with action_buttons[3]: st.button("📞 Call", key="act_call")
    else:
        st.markdown("<p style='padding-top:15px; font-weight:bold; color:red;'>🔒 Upgrade required for bulk actions</p>", unsafe_allow_html=True)
    
    st.markdown("---")

    # 3. FILTER CONTROLS (FUNCTIONAL)
    st.markdown("### Filter Leads & Inventory")
    
    city_options = df_raw['City'].unique().tolist() if not df_raw.empty else ['N/A']
    niche_options = df_raw['Niche'].unique().tolist() if not df_raw.empty else ['N/A']
    reason_options = ['All'] + df_raw['Reason to Contact'].unique().tolist() if not df_raw.empty else ['All']
    
    city_index = city_options.index(st.session_state['user']['city']) if st.session_state['user']['city'] in city_options else 0
    niche_index = niche_options.index(st.session_state['user']['niche']) if st.session_state['user']['niche'] in niche_options else 0
    reason_index = reason_options.index(st.session_state['filter_reason']) if st.session_state['filter_reason'] in reason_options else 0
    
    filter_cols = st.columns(4)
    filter_cols[0].selectbox("City", city_options, key="filter_city", disabled=not is_premium, on_change=st.rerun, index=city_index)
    filter_cols[1].selectbox("Niche", niche_options, key="filter_niche", disabled=not is_premium, on_change=st.rerun, index=niche_index)
    filter_cols[2].slider("Min Score", 0, 100, st.session_state['filter_score'], key="filter_score", disabled=not is_premium, on_change=st.rerun)
    filter_cols[3].selectbox("Reason", reason_options, key="filter_reason", disabled=not is_premium, on_change=st.rerun, index=reason_index)
    
    # 4. LEAD INVENTORY TABLE
    st.markdown("### Lead Inventory (High Priority)")
    
    if total_leads_for_display == 0:
        st.warning("No leads found for your current criteria.")
    else:
        st.dataframe(
            df_filtered_for_display[["Business Name", "Phone", "Email", "Lead Score", "Reason to Contact"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Lead Score": st.column_config.ProgressColumn("Lead Score", format="%d", min_value=0, max_value=100, color="red")
            }
        )


# --- RIGHT COLUMN: OUTREACH & EARNINGS PANEL ---
with main_content_cols[1]:
    
    # 6. OUTREACH TEMPLATES
    with st.container(border=True):
        st.markdown("##### Outreach Templates")
        template_tab1, template_tab2, template_tab3 = st.tabs(["Email", "WhatsApp", "Call Scripts"])
        
        with template_tab1:
            st.caption("Subject: High-Conversion Pitch (Jinja2 Supported)")
            st.text_area("Template Preview", "Hi {{BusinessName}}, I noticed...", height=100, label_visibility="collapsed")
            st.button("Generate & Send (Async)", use_container_width=True, key="send_gen") 

    # 7. POTENTIAL EARNINGS TRACKER
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("##### Probabilistic Conversion Value")
        st.markdown(f"### Estimated Income: **${len(df_filtered_for_display) * 75} Today**")
        st.progress(70) 
        st.caption("Contact more leads to increase earnings!")

    # 8. UPGRADE NUDGE 
    if not is_premium:
        st.markdown("<br>", unsafe_allow_html=True) 
        with st.container(border=True):
            st.markdown("⭐ Unlock Premium Leads")
            st.caption("Get Exclusive High-Value Leads")
            st.button("Upgrade Now", key="upgrade_nudge", use_container_width=True, type="primary")

    # 9. REFERRAL ENGINE
    st.markdown("<br>", unsafe_allow_html=True) 
    with st.container(border=True):
        st.markdown("📞 Earn Referral Bonuses")
        st.caption("Invite Friends & Earn Rewards")
        st.button("Invite & Earn", use_container_width=True, key="invite_nudge", type="primary")
