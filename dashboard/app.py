import streamlit as st
import pandas as pd
from datetime import datetime
import time 

# --------------------------------------------------
# MOCK DATA & CONFIGURATION
# --------------------------------------------------
USER = {
    "name": "John",
    "city": "New York, NY",
    "niche": "Marketing Services",
    "plan": "Pro Plan",
    "credits": 85
}
USER_IS_PREMIUM = True # Set to True to display the full functionality shown in the image

# Define color constants using Hex/names for professional look
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"

# --------------------------------------------------
# MOCK LEADS DATA (Structured to match the image table exactly)
# --------------------------------------------------
leads_data = [
    {
        "Business Name": "BrightStar Marketing", "Phone": "+1 555-123-4567", "Email": "info@brightstarco.com",
        "Lead Score": 92, "Reason to Contact": "New Business in Your Area", "Potential Deal": 500, "Attribute": "New Businesses"
    },
    {
        "Business Name": "GreenLeaf Cafe", "Phone": "+1 555-234-5678", "Email": "contact@greenleafcafe.com",
        "Lead Score": 88, "Reason to Contact": "No Website – Needs Online Presence", "Potential Deal": 750, "Attribute": "No Website"
    },
    {
        "Business Name": "Ace Fitness Center", "Phone": "+1 555-345-6789", "Email": "info@acefitness.com",
        "Lead Score": 85, "Reason to Contact": "High Conversion Potential", "Potential Deal": 1000, "Attribute": "High Conversion"
    },
    {
        "Business Name": "SwiftTech Solutions", "Phone": "+1 555-456-7890", "Email": "sales@swifttechsol.com",
        "Lead Score": 90, "Reason to Contact": "New Startup Seeking Services", "Potential Deal": 500, "Attribute": "New Businesses"
    },
    {
        "Business Name": "Bella Boutique", "Phone": "+1 555-567-8901", "Email": "bella@mailboutique.com",
        "Lead Score": 87, "Reason to Contact": "No Website – Expand Reach", "Potential Deal": 750, "Attribute": "No Website"
    }
]

df = pd.DataFrame(leads_data)

# MOCK KPI DATA for Hero Section
leads_new_biz = len(df[df['Attribute'] == 'New Businesses'])
leads_no_web = len(df[df['Attribute'] == 'No Website'])
leads_high_conv = len(df[df['Attribute'] == 'High Conversion'])


# --------------------------------------------------
# PAGE CONFIG (0)
# --------------------------------------------------
st.set_page_config(
    page_title="Micro Lead Marketplace",
    page_icon="Ⓜ️",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar for max horizontal space
)

# --------------------------------------------------
# 1. TOP HEADER BAR (Integrated Navigation)
# --------------------------------------------------
header_cols = st.columns([0.1, 8, 1, 1, 1])

with header_cols[0]: # Logo/Icon
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Stripe_Logo%2C_revised_2016.svg/1200px-Stripe_Logo%2C_revised_2016.svg.png", width=20) # M-like icon placeholder
with header_cols[1]: # User Info Bar
    st.markdown(
        f"<p style='font-size:12px; margin-top: 10px;'>**Micro B2B Lead Marketplace** | Welcome: {USER['name']} | {USER['city']} | Niche: {USER['niche']} | **{USER['plan']}** | Lead Credits: {USER['credits']}</p>",
        unsafe_allow_html=True
    )
with header_cols[2]:
    st.button("Upgrade Plan", use_container_width=True, key="upgrade_top_bar")
with header_cols[3]:
    st.button("Refer & Earn", type="primary", use_container_width=True, key="refer_top_bar")
with header_cols[4]:
    st.button("≡", use_container_width=True, key="menu_top_bar") 

st.markdown("---")


# --------------------------------------------------
# 2. TODAY'S OPPORTUNITIES (HERO CARDS) & TEMPLATES (SPLIT LAYOUT)
# --------------------------------------------------
st.markdown("## Today’s Best Money Opportunities")

# Main content split: 3/4 for Data & Table, 1/4 for Outreach Panel
main_content_cols = st.columns([9, 3])

# --- LEFT COLUMN: HERO CARDS & TABLE ---
with main_content_cols[0]:
    
    # 2. HERO CARDS
    hero_cols = st.columns(3)
    
    # Helper function for colored card simulation using HTML/CSS
    def render_hero_card(col, title, deal, count, color):
        with col.container(border=True):
            st.markdown(
                f'<div style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">{title}</div>', 
                unsafe_allow_html=True
            )
            st.markdown(f"### {deal}")
            st.markdown(f"**{count}** Leads Available")

    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", 25, COLOR_BLUE) # Using 25 based on image mock
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", 18, COLOR_GREEN) # Using 18 based on image mock
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", 12, COLOR_ORANGE) # Using 12 based on image mock

    # 5. ACTION BAR (Below Hero Cards)
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    with action_buttons[0]: st.button("📥 Download CSV")
    with action_buttons[1]: st.button("📊 Open in Google Sheets")
    with action_buttons[2]: st.button("✉️ Send Email")
    with action_buttons[3]: st.button("📞 Call")
    
    st.markdown("---")

    # 4. LEADS TABLE (Action-Oriented)
    st.dataframe(
        df[["Business Name", "Phone", "Email", "Lead Score", "Reason to Contact"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Lead Score": st.column_config.ProgressColumn("Lead Score", format="%d", min_value=0, max_value=100)
        }
    )

# --- RIGHT COLUMN: OUTREACH & EARNINGS PANEL ---
with main_content_cols[1]:
    
    # 6. OUTREACH TEMPLATES
    with st.container(border=True):
        st.markdown("##### Outreach Templates")
        # Tabs for Email, WhatsApp, Call Scripts
        template_tab1, template_tab2, template_tab3 = st.tabs(["Email", "WhatsApp", "Call Scripts"])
        
        with template_tab1:
            st.text_area("Template Preview", "Subject: High-Conversion Pitch\n\nHi {{BusinessName}}, I noticed...", height=150, label_visibility="collapsed")
            st.button("Generate & Send", use_container_width=True)

    # 7. POTENTIAL EARNINGS TRACKER
    with st.container(border=True):
        st.markdown("##### Potential Earnings")
        st.markdown("### Estimated Income: **$3,750 Today**")
        st.progress(70) # Simulate a progress bar (70% reached)
        st.caption("Contact more leads to increase earnings!")


    # 8. UPGRADE NUDGE / 9. REFERRAL ENGINE (Bottom Cards)
    st.markdown("---")
    
    # Card 1: Unlock Premium Leads
    with st.container(border=True):
        nudge_cols = st.columns([1, 2])
        with nudge_cols[0]:
            st.markdown("⭐", help="Star Icon Simulation", unsafe_allow_html=True)
        with nudge_cols[1]:
            st.markdown("##### Unlock Premium Leads")
            st.caption("Get Exclusive High-Value Leads")
            st.button("Upgrade Now", type="primary", use_container_width=True)

    # Card 2: Earn Referral Bonuses
    with st.container(border=True):
        referral_cols = st.columns([1, 2])
        with referral_cols[0]:
            st.markdown("📞", help="Phone Icon Simulation", unsafe_allow_html=True)
        with referral_cols[1]:
            st.markdown("##### Earn Referral Bonuses")
            st.caption("Invite Friends & Earn Rewards")
            st.button("Invite & Earn", use_container_width=True)
