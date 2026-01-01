import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --------------------------------------------------
# CONFIGURATION & USER STATE
# --------------------------------------------------
USER = {
    "name": "Ravi Kumar",
    "city": "Pune, India",
    "niche": "Marketing Services",
    "plan": "Pro Plan",
    "credits": 85
}
USER_IS_PREMIUM = True 

# Define color constants (Used for Hero Cards and CTAs)
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"
COLOR_RED_CTA = "#f87171" 

# --- HELPER FUNCTIONS ---

def mask_email(email):
    """PII Masking function."""
    if '@' in email and len(email.split('@')[0]) > 4:
        username, domain = email.split('@')
        return f"{username[:2]}****@{domain}"
    return email

def mask_phone(phone):
    """PII Masking function."""
    if len(phone) > 8:
        return f"{phone[:8]}***-{phone[-4:]}"
    return phone

def render_hero_card(col, title, deal, count, color):
    """Renders a single, color-coded KPI card."""
    with col.container(border=True, height=140):
        st.markdown(
            f'<div style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 14px;">{title}</div>', 
            unsafe_allow_html=True
        )
        st.markdown(f"**{deal}**", unsafe_allow_html=True)
        st.markdown(f"**{count}** Leads Available", help="Count of leads available for this segment.")


# --------------------------------------------------
# MOCK LEADS DATA (Structured and ready for display)
# --------------------------------------------------
leads_data = [
    {
        "Business Name": "BrightStar Marketing", "Phone": "+1 555-123-4567", "Email": "info@brightstarco.com",
        "Lead Score": 92, "Reason to Contact": "New Business in Your Area", "Attribute": "New Businesses", "Potential Deal": 500
    },
    {
        "Business Name": "GreenLeaf Cafe", "Phone": "+1 555-234-5678", "Email": "contact@greenleafcafe.com",
        "Lead Score": 70, "Reason to Contact": "No Website – Needs Online Presence", "Attribute": "No Website", "Potential Deal": 750
    },
    {
        "Business Name": "Ace Fitness Center", "Phone": "+1 555-345-6789", "Email": "info@acefitness.com",
        "Lead Score": 85, "Reason to Contact": "High Conversion Potential", "Attribute": "High Conversion", "Potential Deal": 1000
    },
    {
        "Business Name": "SwiftTech Solutions", "Phone": "+1 555-456-7890", "Email": "sales@swifttechsol.com",
        "Lead Score": 90, "Reason to Contact": "New Startup Seeking Services", "Attribute": "New Businesses", "Potential Deal": 500
    },
    {
        "Business Name": "Bella Boutique", "Phone": "+1 555-567-8901", "Email": "bella@mailboutique.com",
        "Lead Score": 65, "Reason to Contact": "No Website – Expand Reach", "Attribute": "No Website", "Potential Deal": 750
    }
]

df_raw = pd.DataFrame(leads_data)

# APPLY PII MASKING (Essential for security and compliance simulation)
df_raw['Phone'] = df_raw['Phone'].apply(mask_phone)
df_raw['Email'] = df_raw['Email'].apply(mask_email)

# MOCK KPI DATA CALCULATION
leads_new_biz = len(df_raw[df_raw['Attribute'] == 'New Businesses'])
leads_no_web = len(df_raw[df_raw['Attribute'] == 'No Website'])
leads_high_conv = len(df_raw[df_raw['Attribute'] == 'High Conversion'])


# --------------------------------------------------
# GLOBAL CSS INJECTION (Density and Aesthetics)
# --------------------------------------------------
st.markdown(f"""
<style>
/* 1. Adjust spacing for density */
.stApp {{ padding-top: 20px !important; padding-right: 30px !important; padding-left: 30px !important; }}
div[data-testid="stVerticalBlock"] > div:first-child {{ padding-top: 0 !important; }}
.st-emotion-cache-1mnrbfp {{ visibility: hidden !important; }}

/* 2. FIX: Primary Button Color (Overrides Streamlit's default blue to RED) */
.stButton>button[kind="primary"] {{
    background-color: {COLOR_RED_CTA} !important;
    color: white !important;
    border: none !important;
}}

/* 3. FIX: Header Button Alignment (Targets specific columns for vertical alignment) */
.header-buttons-container {{
    display: flex;
    align-items: center; 
    height: 100%; 
}}

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


# 1. TOP HEADER BAR (FINAL PROFESSIONAL FIX)
header_cols = st.columns([0.1, 7, 1, 1, 0.5]) 

with header_cols[0]: # Logo/Icon
    st.markdown("Ⓜ️") 
    
with header_cols[1]: # User Info Bar (Cleaned and compacted)
    meta_cols = st.columns([2, 1.5, 2, 1.5])
    
    with meta_cols[0]:
        st.markdown(f"**Micro B2B Lead Marketplace**", unsafe_allow_html=True)
    with meta_cols[1]:
        st.caption(f"Welcome: {USER['name']}")
    with meta_cols[2]:
        st.caption(f"{USER['city']} | Niche: {USER['niche']}")
    with meta_cols[3]:
        st.caption(f"**{USER['plan']}** | Credits: {USER['credits']}")

# --- RIGHT BUTTONS (FIXED HORIZONTAL LAYOUT AND COLOR) ---
# We force the buttons to be horizontal and use primary style for consistency.

with header_cols[2]:
    st.button("Upgrade Plan", key="upgrade_top_bar")

with header_cols[3]:
    # Refer & Earn uses type="primary" to be red
    st.button("Refer & Earn", key="refer_top_bar", type="primary")

with header_cols[4]:
    st.button("☰", use_container_width=True, key="menu_top_bar") 

st.markdown("---")


# --------------------------------------------------
# 2. TODAY'S OPPORTUNITIES (HERO CARDS) & TEMPLATES
# --------------------------------------------------
st.markdown("## Today’s Best Money Opportunities")

main_content_cols = st.columns([9, 3])

# --- LEFT COLUMN: HERO CARDS & TABLE ---
with main_content_cols[0]:
    
    hero_cols = st.columns(3)
    
    # Hero Card Calls (Stable and Fixed)
    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", leads_new_biz, COLOR_BLUE)
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", leads_no_web, COLOR_GREEN)
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", leads_high_conv, COLOR_ORANGE)

    # 5. ACTION BAR 
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    with action_buttons[0]: st.button("📥 Download CSV", key="act_csv")
    with action_buttons[1]: st.button("📊 Open in Google Sheets", key="act_sheets")
    with action_buttons[2]: st.button("✉️ Send Email", key="act_email")
    with action_buttons[3]: st.button("📞 Call", key="act_call")
    
    st.markdown("<br>", unsafe_allow_html=True) 

    # 4. LEAD INVENTORY TABLE
    st.markdown("### Lead Inventory (High Priority)")
    
    df_table_view = df_raw[["Business Name", "Phone", "Email", "Lead Score", "Reason to Contact"]].copy()

    st.dataframe(
        df_table_view,
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
        st.markdown("### Estimated Income: **$3,750 Today**")
        st.progress(70) 
        st.caption("Contact more leads to increase earnings!")

    # 8. UPGRADE NUDGE (Button Color Fixed)
    st.markdown("<br>", unsafe_allow_html=True) 
    with st.container(border=True):
        st.markdown("⭐ Unlock Premium Leads")
        st.caption("Get Exclusive High-Value Leads")
        # Uses type="primary" which is globally red
        st.button("Upgrade Now", key="upgrade_nudge", use_container_width=True, type="primary")

    # 9. REFERRAL ENGINE (Button Color Fixed)
    st.markdown("<br>", unsafe_allow_html=True) 
    with st.container(border=True):
        st.markdown("📞 Earn Referral Bonuses")
        st.caption("Invite Friends & Earn Rewards")
        # Uses type="primary" which is globally red
        st.button("Invite & Earn", key="invite_nudge", use_container_width=True, type="primary")
