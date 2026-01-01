import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --------------------------------------------------
# CONFIGURATION & USER STATE MANAGEMENT
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

# --- SESSION STATE INITIALIZATION ---
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
        # Reset filters to show all for premium user initially
        st.session_state['filter_city'] = 'All'
        st.session_state['filter_niche'] = 'All'
        st.session_state['filter_score'] = 0 # Lower to show more leads
        st.session_state['filter_reason'] = 'All'
        st.rerun() 
        return True
    elif key == TRIAL_KEY:
        st.session_state['logged_in'] = True
        st.session_state['is_premium'] = False
        st.session_state['user'] = {"name": "New Trialist", "city": "Pune, India", "niche": "Grocery Stores", "plan": "Trial", "credits": 10}
        # For trial, set default filters to match their limited view
        st.session_state['filter_city'] = 'Pune, India'
        st.session_state['filter_niche'] = 'Grocery Stores'
        st.session_state['filter_score'] = 70 # Default min score
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

# --- HELPER FUNCTIONS ---
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

# --------------------------------------------------
# MOCK LEADS DATA (Full Definition)
# --------------------------------------------------
leads_data = [
    { "Business Name": "BrightStar Marketing", "Phone": "+91 988-123-4567", "Email": "info@brightstarco.com", "Lead Score": 92, "Reason to Contact": "New Business in Your Area", "Attribute": "New Businesses", "Potential Deal": 500, "City": "Pune, India", "Niche": "Grocery Stores" },
    { "Business Name": "Fresh Mart Deli", "Phone": "+91 876-234-5678", "Email": "deli@freshmart.in", "Lead Score": 88, "Reason to Contact": "No Website – Needs Online Presence", "Attribute": "No Website", "Potential Deal": 750, "City": "Pune, India", "Niche": "Grocery Stores" },
    { "Business Name": "Quality Grocers", "Phone": "+91 900-345-6789", "Email": "quality@grocers.com", "Lead Score": 85, "Reason to Contact": "High Conversion Potential", "Attribute": "High Conversion", "Potential Deal": 1000, "City": "Pune, India", "Niche": "Grocery Stores" },
    { "Business Name": "Swift Supplies Co.", "Phone": "+91 765-456-7890", "Email": "sales@swift.in", "Lead Score": 90, "Reason to Contact": "New Startup Seeking Services", "Attribute": "New Businesses", "Potential Deal": 500, "City": "Pune, India", "Niche": "Grocery Stores" },
    { "Business Name": "Bella Boutique", "Phone": "+91 999-567-8901", "Email": "bella@mailboutique.com", "Lead Score": 87, "Reason to Contact": "No Website – Expand Reach", "Attribute": "No Website", "Potential Deal": 750, "City": "Pune, India", "Niche": "Grocery Stores" },
    { "Business Name": "Sea View Diner", "Phone": "+91 111-567-8901", "Email": "diner@sea.com", "Lead Score": 65, "Reason to Contact": "Poor Reviews – Easy Pitch", "Attribute": "Poor Reviews", "Potential Deal": 500, "City": "Mumbai", "Niche": "Restaurants" },
    { "Business Name": "The Curry Pot", "Phone": "+91 222-567-8901", "Email": "curry@pot.com", "Lead Score": 95, "Reason to Contact": "High Revenue Potential", "Attribute": "High Conversion", "Potential Deal": 1500, "City": "Mumbai", "Niche": "Restaurants" },
    { "Business Name": "Global Mart", "Phone": "+91 333-567-8901", "Email": "global@mart.com", "Lead Score": 75, "Reason to Contact": "New Digital Gap", "Attribute": "No Website", "Potential Deal": 800, "City": "Delhi", "Niche": "Grocery Stores" },
    { "Business Name": "Local HVAC", "Phone": "+1 555-555-0000", "Email": "hvac@local.com", "Lead Score": 60, "Reason to Contact": "Standard Lead", "Attribute": "Other", "Potential Deal": 300, "City": "Dallas, TX", "Niche": "HVAC Services" }
]
df_raw = pd.DataFrame(leads_data)

# MOCK KPI DATA CALCULATION (These counts are from the FULL df_raw, not filtered)
leads_new_biz_count = len(df_raw[df_raw['Attribute'] == 'New Businesses'])
leads_no_web_count = len(df_raw[df_raw['Attribute'] == 'No Website'])
leads_high_conv_count = len(df_raw[df_raw['Attribute'] == 'High Conversion'])


# --------------------------------------------------
# GLOBAL CSS INJECTION (Stable Styling)
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
with header_cols[2]: st.button("Upgrade Plan", key="upgrade_top_bar")
with header_cols[3]: st.button("Refer & Earn", key="refer_top_bar", type="primary")
with header_cols[4]: st.button("☰", use_container_width=True, key="menu_top_bar", on_click=logout) 

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
df_current_view = df_raw.copy() # Start with the full raw data

is_premium = st.session_state['is_premium']

# Apply filters based on session state for PREMIUM users
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
    df_filtered_for_display = df_current_view # Premium users see all filtered leads
else:
    # Trial Logic: Enforce Ravi's default niche and limit leads
    df_current_view = df_current_view[df_current_view['City'] == st.session_state['user']['city']]
    df_current_view = df_current_view[df_current_view['Niche'] == st.session_state['user']['niche']]
    
    total_leads_for_display = len(df_current_view) # Count before limiting for message
    df_filtered_for_display = df_current_view.head(TRIAL_LEAD_LIMIT) # Trial users see only a subset


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
    
    city_options = df_raw['City'].unique().tolist()
    niche_options = df_raw['Niche'].unique().tolist()
    reason_options = ['All'] + df_raw['Reason to Contact'].unique().tolist()
    
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
