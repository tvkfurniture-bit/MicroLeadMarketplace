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
USER_IS_PREMIUM = True # Set to True for the full dashboard view

# Define color constants
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"

# --- HELPER FUNCTIONS FOR DATA MASKING (Requirement 7) ---

def mask_email(email):
    # PII Masking: Ex: info@brightstarco.com -> info@mail****.com
    if '@' in email and len(email.split('@')[0]) > 4:
        username, domain = email.split('@')
        return f"{username[:4]}****@{domain}"
    return email

def mask_phone(phone):
    # PII Masking: Ex: +1 555-123-4567 -> +1 555-***-4567
    if len(phone) > 8:
        return f"{phone[:8]}***-{phone[-4:]}"
    return phone

# --- RENDER FUNCTION (FIXES NameError) ---
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
# MOCK LEADS DATA (Structured to match the image table exactly)
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

# ENRICHMENT AND MASKING FOR DISPLAY
df_raw['Phone'] = df_raw['Phone'].apply(mask_phone) # Mask PII for default display
df_raw['Email'] = df_raw['Email'].apply(mask_email)
df_raw['Reason to Contact'] = df_raw['Reason to Contact'].str.wrap(30) # Wrap long text
df_raw['Lead Score'] = df_raw['Lead Score'] # Keep score as is for progress bar

# MOCK KPI DATA CALCULATION (Used in Hero Cards)
leads_new_biz = len(df_raw[df_raw['Attribute'] == 'New Businesses'])
leads_no_web = len(df_raw[df_raw['Attribute'] == 'No Website'])
leads_high_conv = len(df_raw[df_raw['Attribute'] == 'High Conversion'])


# --------------------------------------------------
# GLOBAL CSS INJECTION (Density Fixes)
# --------------------------------------------------
st.markdown("""
<style>
/* Adjust top padding and content width */
.stApp { padding-top: 20px !important; padding-right: 30px !important; padding-left: 30px !important; }
/* Remove excessive vertical spacing */
div[data-testid="stVerticalBlock"] > div:first-child { padding-top: 0 !important; }
/* Reduce padding in table rows for high density */
.stDataFrame table td { padding: 4px 10px !important; } 
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 1. TOP HEADER BAR (Integrated Navigation)
# --------------------------------------------------
header_cols = st.columns([0.1, 8, 1, 1, 1])

with header_cols[0]: 
    st.markdown("Ⓜ️") # Simple icon
with header_cols[1]: 
    st.markdown(
        f"<p style='font-size:12px; margin-top: 10px;'>**Micro B2B Lead Marketplace** | Welcome: {USER['name']} | {USER['city']} | Niche: {USER['niche']} | **{USER['plan']}** | Lead Credits: {USER['credits']}</p>",
        unsafe_allow_html=True
    )
with header_cols[2]:
    st.button("Upgrade Plan", use_container_width=True, key="upgrade_top_bar")
with header_cols[3]:
    st.button("Refer & Earn", type="primary", use_container_width=True, key="refer_top_bar")
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
    
    # Hero Card Calls (FIXED NameError)
    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", leads_new_biz, COLOR_BLUE)
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", leads_no_web, COLOR_GREEN)
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", leads_high_conv, COLOR_ORANGE)

    # 5. ACTION BAR (Directly below cards)
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    with action_buttons[0]: st.button("📥 Download CSV", key="act_csv")
    with action_buttons[1]: st.button("📊 Open in Google Sheets", key="act_sheets")
    with action_buttons[2]: st.button("✉️ Send Email", key="act_email")
    with action_buttons[3]: st.button("📞 Call", key="act_call")
    
    st.markdown("<br>", unsafe_allow_html=True) 

    # 4. LEAD INVENTORY TABLE
    st.markdown("### Lead Inventory (High Priority)")
    
    # We select the columns needed for the final display
    df_table_view = df_raw[["Business Name", "Phone", "Email", "Lead Score", "Reason to Contact"]].copy()

    st.dataframe(
        df_table_view,
        use_container_width=True,
        hide_index=True,
        column_config={
            # Lead Score Visualization (Uses custom red bar visualization required by design)
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

    # 7. POTENTIAL EARNINGS TRACKER (Simulating the final metric card)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("##### Probabilistic Conversion Value")
        st.markdown("### Estimated Income: **$3,750 Today**")
        st.progress(70) 
        st.caption("Contact more leads to increase earnings!")

    # 8. UPGRADE NUDGE (Simplified Card)
    st.markdown("<br>", unsafe_allow_html=True) 
    with st.container(border=True):
        st.markdown("⭐ Unlock Premium Leads")
        st.caption("Get Exclusive High-Value Leads")
        st.button("Upgrade Now", use_container_width=True, type="primary")

    # 9. REFERRAL ENGINE (Simplified Card)
    st.markdown("<br>", unsafe_allow_html=True) 
    with st.container(border=True):
        st.markdown("📞 Earn Referral Bonuses")
        st.caption("Invite Friends & Earn Rewards")
        st.button("Invite & Earn", use_container_width=True)
