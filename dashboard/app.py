import streamlit as st
import pandas as pd
import numpy as np
# Note: Base64 and time imports removed as they were not strictly required for the final design logic.

# --------------------------------------------------
# CONFIGURATION & MOCK DATA SETUP
# --------------------------------------------------
# Define color constants (used for card backgrounds)
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"
COLOR_LIGHT_GREY = "#f9fafb"

# MOCK USER DATA (Matched to image)
USER = {
    "name": "John",
    "city": "New York, NY",
    "niche": "Marketing Services",
    "plan": "Pro Plan",
    "credits": 85
}
USER_IS_PREMIUM = True 

# MOCK LEADS DATA (Structured to match the image table exactly)
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

# --- FUNCTIONAL UTILITIES ---

# Function to simulate the color badge for Lead Score (HTML Injection)
def get_score_style(score):
    if score >= 90:
        color = "darkgreen"
    elif score >= 85:
        color = "orange"
    else:
        color = "red"
    # Returns HTML/Markdown code that Streamlit will render as text with color
    return f'<div style="background-color: {color}; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; display: inline-block;">{score}</div>'

# Apply the style function to the dataframe for display
df['Lead Score'] = df['Lead Score'].apply(get_score_style)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Micro Lead Marketplace",
    page_icon="Ⓜ️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# 1. TOP HEADER BAR (Integrated Navigation)
# --------------------------------------------------
logo_html = f"""
    <div style='display: flex; align-items: center; gap: 8px; font-size: 14px;'>
        <span style='color: {COLOR_BLUE}; font-size: 20px; font-weight: bold;'>M</span> 
        Micro B2B Lead Marketplace 
        <span style='margin-left: 20px;'>Welcome: {USER['name']} | {USER['city']} | Niche: {USER['niche']} | <b>{USER['plan']}</b> | Lead Credits: {USER['credits']}</span>
    </div>
"""
header_cols = st.columns([1, 8, 1, 1, 1])

with header_cols[0]: # Logo/Icon
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Stripe_Logo%2C_revised_2016.svg/1200px-Stripe_Logo%2C_revised_2016.svg.png", width=20) 
with header_cols[1]: # User Info Bar
    st.markdown(logo_html, unsafe_allow_html=True)
with header_cols[2]:
    st.button("Upgrade Plan", use_container_width=True, key="upgrade_top_bar")
with header_cols[3]:
    st.button("Refer & Earn", type="primary", use_container_width=True, key="refer_top_bar")
with header_cols[4]:
    st.button("☰", use_container_width=True, key="menu_top_bar") 

st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True) 


# --------------------------------------------------
# 2. TODAY'S OPPORTUNITIES (HERO CARDS) & TEMPLATES
# --------------------------------------------------
st.markdown("## Today’s Best Money Opportunities")

main_content_cols = st.columns([9, 3])

# --- LEFT COLUMN: HERO CARDS & ACTION BAR ---
with main_content_cols[0]:
    
    hero_cols = st.columns(3)
    
    # Helper function for rendering cards with specific colors/text
    def render_saas_card(col, title, deal, count, color_hex):
        with col.container(border=False):
            st.markdown(
                f'<div style="background: linear-gradient(135deg, {color_hex} 0%, #374151 100%); color: white; padding: 15px; border-radius: 8px; font-weight: bold; height: 120px;">'
                f'<div style="font-size: 16px;">{title}</div>'
                f'<div style="font-size: 24px; margin-top: 5px;">{deal}</div>'
                f'<div style="font-size: 14px; opacity: 0.8;">{count} Leads Available</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    render_saas_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", 25, COLOR_BLUE) 
    render_saas_card(hero_cols[1], "No Website", "$750+ Potential Deal", 18, COLOR_GREEN) 
    render_saas_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", 12, COLOR_ORANGE) 

    # 5. ACTION BAR (Below Hero Cards)
    st.markdown("<br>", unsafe_allow_html=True)
    action_buttons = st.columns([1.5, 2, 1.5, 1])

    with action_buttons[0]: st.button("Download CSV", use_container_width=True, key="download_bttn")
    with action_buttons[1]: st.button("Open in Google Sheets", use_container_width=True, key="sheets_bttn")
    with action_buttons[2]: st.button("Send Email", use_container_width=True, key="email_bttn")
    with action_buttons[3]: st.button("Call", use_container_width=True, key="call_bttn")
    st.markdown("---")


    # 4. LEADS TABLE
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        # -----------------------------------------------------------
        # CRITICAL FIX FOR TYPEERROR: ALLOW HTML RENDERING IN DATAFRAME
        # -----------------------------------------------------------
        unsafe_allow_html=True, 
    )

# --- RIGHT COLUMN: OUTREACH & EARNINGS PANEL ---
with main_content_cols[1]:
    
    # 6. OUTREACH TEMPLATES (Tabs)
    with st.container(border=True):
        st.markdown("##### Outreach Templates")
        template_tab1, template_tab2, template_tab3 = st.tabs(["Email", "WhatsApp", "Call Scripts"])
        
        with template_tab1:
            st.text_area("Template Preview", "Subject: High-Conversion Pitch\n\nHi {{BusinessName}}, I noticed...", height=150, label_visibility="collapsed")
            st.button("Generate & Send", use_container_width=True, type="secondary")

    # 7. POTENTIAL EARNINGS TRACKER
    with st.container(border=True):
        st.markdown("##### Potential Earnings")
        st.markdown("### Estimated Income: **$3,750 Today**")
        st.progress(70) 
        st.caption("Contact more leads to increase earnings!")


    # 8. UPGRADE NUDGE (Bottom Left Card)
    st.markdown("---")
    with st.container(border=True):
        nudge_cols = st.columns([1, 2])
        with nudge_cols[0]:
            st.markdown("⭐", help="Star Icon Simulation", unsafe_allow_html=True)
        with nudge_cols[1]:
            st.markdown("##### Unlock Premium Leads")
            st.caption("Get Exclusive High-Value Leads")
            st.button("Upgrade Now", use_container_width=True, type="primary")

    # 9. REFERRAL ENGINE (Bottom Right Card)
    with st.container(border=True):
        referral_cols = st.columns([1, 2])
        with referral_cols[0]:
            st.markdown("📞", help="Phone Icon Simulation", unsafe_allow_html=True)
        with referral_cols[1]:
            st.markdown("##### Earn Referral Bonuses")
            st.caption("Invite Friends & Earn Rewards")
            st.button("Invite & Earn", use_container_width=True, type="secondary")
