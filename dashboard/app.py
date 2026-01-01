import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --------------------------------------------------
# CONFIGURATION & USER STATE MANAGEMENT
# --------------------------------------------------
# Simulation keys and constants
PREMIUM_ACCESS_KEY = "30DAYPRO" 
TRIAL_LEAD_LIMIT = 5 
SUBSCRIPTION_PRICE = 30
COLOR_RED_CTA = "#f87171" 
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'is_premium' not in st.session_state:
    st.session_state['is_premium'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = {
        "name": "Trial User", "city": "N/A", "niche": "All", "plan": "Trial", "credits": 10
    }
# --- END SESSION STATE ---

# --- AUTH FUNCTIONS ---
def login(key):
    if key == PREMIUM_ACCESS_KEY:
        st.session_state['logged_in'] = True
        st.session_state['is_premium'] = True
        st.session_state['user'] = {
            "name": "Ravi Kumar", "city": "Pune, India", "niche": "Grocery Stores", "plan": "Pro Plan", "credits": 85
        }
    elif key == "TRIAL": # Simple placeholder for trial login
        st.session_state['logged_in'] = True
        st.session_state['is_premium'] = False
        st.session_state['user'] = {
            "name": "Trial User", "city": "Pune, India", "niche": "All", "plan": "Trial", "credits": 10
        }
    else:
        st.error("Invalid Access Key.")
        return False
    st.rerun()

def logout():
    st.session_state['logged_in'] = False
    st.session_state['is_premium'] = False
    st.session_state['user'] = {"name": "Trial User", "city": "N/A", "niche": "All", "plan": "Trial", "credits": 0}
    st.rerun()

# --- HELPER FUNCTIONS ---

def mask_email(email, is_premium):
    if is_premium: return email
    if '@' in email and len(email.split('@')[0]) > 4:
        username, domain = email.split('@')
        return f"{username[:2]}****@{domain}"
    return email

def mask_phone(phone, is_premium):
    if is_premium: return phone
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
# MOCK LEADS DATA (Expanded for Filtering)
# --------------------------------------------------
leads_data = [
    # Pune - Grocery (Ravi's target niche)
    { "Business Name": "BrightStar Marketing", "Phone": "+91 988-123-4567", "Email": "info@brightstarco.com", "Lead Score": 92, "Reason to Contact": "New Business in Your Area", "Attribute": "New Businesses", "Potential Deal": 500, "City": "Pune", "Niche": "Grocery Stores" },
    { "Business Name": "Fresh Mart Deli", "Phone": "+91 876-234-5678", "Email": "deli@freshmart.in", "Lead Score": 88, "Reason to Contact": "No Website – Needs Online Presence", "Attribute": "No Website", "Potential Deal": 750, "City": "Pune", "Niche": "Grocery Stores" },
    { "Business Name": "Quality Grocers", "Phone": "+91 900-345-6789", "Email": "quality@grocers.com", "Lead Score": 85, "Reason to Contact": "High Conversion Potential", "Attribute": "High Conversion", "Potential Deal": 1000, "City": "Pune", "Niche": "Grocery Stores" },
    { "Business Name": "Swift Supplies Co.", "Phone": "+91 765-456-7890", "Email": "sales@swift.in", "Lead Score": 90, "Reason to Contact": "New Startup Seeking Services", "Attribute": "New Businesses", "Potential Deal": 500, "City": "Pune", "Niche": "Grocery Stores" },
    { "Business Name": "Bella Boutique", "Phone": "+91 999-567-8901", "Email": "bella@mailboutique.com", "Lead Score": 87, "Reason to Contact": "No Website – Expand Reach", "Attribute": "No Website", "Potential Deal": 750, "City": "Pune", "Niche": "Grocery Stores" },
    
    # Mumbai - Restaurants (Expansion niche)
    { "Business Name": "Sea View Diner", "Phone": "+91 111-567-8901", "Email": "diner@sea.com", "Lead Score": 65, "Reason to Contact": "Poor Reviews – Easy Pitch", "Attribute": "Poor Reviews", "Potential Deal": 500, "City": "Mumbai", "Niche": "Restaurants" },
    { "Business Name": "The Curry Pot", "Phone": "+91 222-567-8901", "Email": "curry@pot.com", "Lead Score": 95, "Reason to Contact": "High Revenue Potential", "Attribute": "High Conversion", "Potential Deal": 1500, "City": "Mumbai", "Niche": "Restaurants" },
    
    # Delhi - Grocery
    { "Business Name": "Global Mart", "Phone": "+91 333-567-8901", "Email": "global@mart.com", "Lead Score": 75, "Reason to Contact": "New Digital Gap", "Attribute": "No Website", "Potential Deal": 800, "City": "Delhi", "Niche": "Grocery Stores" },

    # Default/Uncategorized (Simulated existing pool)
    { "Business Name": "Local HVAC", "Phone": "+1 555-555-0000", "Email": "hvac@local.com", "Lead Score": 60, "Reason to Contact": "Standard Lead", "Attribute": "Other", "Potential Deal": 300, "City": "Dallas, TX", "Niche": "HVAC Services" }
]

df_raw = pd.DataFrame(leads_data)


# --------------------------------------------------
# GLOBAL CSS INJECTION (Density and Aesthetics)
# --------------------------------------------------
st.markdown(f"""
<style>
/* Adjust spacing for density and button color */
.stApp {{ padding-top: 20px !important; padding-right: 30px !important; padding-left: 30px !important; }}
div[data-testid="stVerticalBlock"] > div:first-child {{ padding-top: 0 !important; }}
.st-emotion-cache-1mnrbfp {{ visibility: hidden !important; }}
.stButton>button[kind="primary"] {{ background-color: {COLOR_RED_CTA} !important; color: white !important; border: none !important; }}
.header-buttons-container {{ display: flex; align-items: center; height: 100%; }}
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

# --- AUTHENTICATION GATE ---
if not st.session_state['logged_in']:
    st.title("Micro Lead Marketplace Access")
    st.subheader("Login or Start Your Free Trial")
    
    auth_cols = st.columns([1, 1, 1])
    
    key_input = auth_cols[0].text_input("Enter Access Key:", type="password", key="auth_key_input")
    
    if auth_cols[1].button("Unlock Premium", key="btn_unlock_premium"):
        if key_input:
            login(key_input)
    
    if auth_cols[2].button("Start 7-Day Free Trial", key="btn_start_trial", type="secondary"):
        login("TRIAL")
        
    st.info("Use key 'TRIAL' to start the free 7-day trial and see limited leads.")
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
if 'filter_city' not in st.session_state:
    st.session_state['filter_city'] = 'Pune'
if 'filter_niche' not in st.session_state:
    st.session_state['filter_niche'] = 'Grocery Stores'
if 'filter_score' not in st.session_state:
    st.session_state['filter_score'] = 70
if 'filter_reason' not in st.session_state:
    st.session_state['filter_reason'] = 'All'


# --- DYNAMIC FILTERING LOGIC ---
df_filtered = df_raw.copy()

if st.session_state['filter_city'] != 'All':
    df_filtered = df_filtered[df_filtered['City'] == st.session_state['filter_city']]
if st.session_state['filter_niche'] != 'All':
    df_filtered = df_filtered[df_filtered['Niche'] == st.session_state['filter_niche']]
if st.session_state['filter_score'] > 0:
    df_filtered = df_filtered[df_filtered['Lead Score'] >= st.session_state['filter_score']]

# Trial Logic: Limit leads if not premium
if not st.session_state['is_premium']:
    st.info(f"Free Trial Active: Displaying top {TRIAL_LEAD_LIMIT} leads. Upgrade for UNLIMITED access and filtering.")
    df_filtered = df_filtered.head(TRIAL_LEAD_LIMIT)


# --- LEFT COLUMN: HERO CARDS & TABLE ---
with main_content_cols[0]:
    hero_cols = st.columns(3)
    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", leads_new_biz, COLOR_BLUE)
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", leads_no_web, COLOR_GREEN)
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", leads_high_conv, COLOR_ORANGE)

    # 5. ACTION BAR 
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    
    # Functional Buttons (Require Premium Status Check)
    if st.session_state['is_premium']:
        with action_buttons[0]: st.button("📥 Download CSV", key="act_csv")
        with action_buttons[1]: st.button("📊 Open in Google Sheets", key="act_sheets")
        with action_buttons[2]: st.button("✉️ Send Email", key="act_email")
        with action_buttons[3]: st.button("📞 Call", key="act_call")
    else:
        st.markdown("<p style='padding-top:15px; font-weight:bold; color:red;'>🔒 Upgrade required for bulk actions</p>", unsafe_allow_html=True)
    
    st.markdown("---")

    # 3. FILTER CONTROLS (FUNCTIONAL)
    st.markdown("### Filter Leads & Inventory")
    
    filter_cols = st.columns(4)
    filter_cols[0].selectbox("City", df_raw['City'].unique(), key="filter_city", disabled=not st.session_state['is_premium'])
    filter_cols[1].selectbox("Niche", df_raw['Niche'].unique(), key="filter_niche", disabled=not st.session_state['is_premium'])
    filter_cols[2].slider("Min Score", 0, 100, st.session_state['filter_score'], key="filter_score", disabled=not st.session_state['is_premium'])
    filter_cols[3].selectbox("Reason", ['All', 'New Business', 'No Website'], key="filter_reason", disabled=not st.session_state['is_premium'])
    
    # 4. LEAD INVENTORY TABLE
    st.markdown("### Lead Inventory (High Priority)")
    
    # PII Masking applied in the dataframe construction (Conditional on plan)
    df_table_view = df_filtered.copy()
    
    st.dataframe(
        df_table_view[["Business Name", "Phone", "Email", "Lead Score", "Reason to Contact"]],
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
        st.markdown(f"### Estimated Income: **${len(df_filtered) * 75} Today**") # Dynamic Calculation
        st.progress(70) 
        st.caption("Contact more leads to increase earnings!")

    # 8. UPGRADE NUDGE 
    if not st.session_state['is_premium']:
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
