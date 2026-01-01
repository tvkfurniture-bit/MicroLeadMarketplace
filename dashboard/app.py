import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
# Use 'collapsed' sidebar for maximum screen real estate
st.set_page_config(
    page_title="Micro Lead Marketplace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --------------------------------------------------
# CUSTOM CSS INJECTION (FOR DENSITY AND CLEAN LOOK)
# --------------------------------------------------
st.markdown("""
<style>
/* 1. Remove Streamlit's default padding */
.stApp {
    padding-top: 20px !important;
    padding-right: 30px !important;
    padding-left: 30px !important;
}

/* 2. Reduce vertical spacing around block elements (headers, charts) */
div[data-testid="stVerticalBlock"] > div:first-child {
    padding-top: 0 !important;
}

/* 3. Style the colored KPI cards for better integration */
.st-emotion-cache-1mnrbfp {
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MOCK DATA & CONFIGURATION
# --------------------------------------------------
USER = {
    "name": "Ravi Kumar",
    "city": "Pune, India",
    "niche": "Marketing Services",
    "plan": "Pro Plan",
    "credits": 85
}
USER_IS_PREMIUM = True 

# Define color constants (Used for KPI boxes)
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"

# --- MOCK LEADS DATA (Using a clean structure) ---
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

# MOCK KPI DATA CALCULATION
leads_new_biz = len(df[df['Attribute'] == 'New Businesses'])
leads_no_web = len(df[df['Attribute'] == 'No Website'])
leads_high_conv = len(df[df['Attribute'] == 'High Conversion'])


# --------------------------------------------------
# 1. TOP HEADER BAR (Integrated Navigation)
# --------------------------------------------------
header_cols = st.columns([0.1, 8, 1, 1, 1])

with header_cols[0]: 
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Stripe_Logo%2C_revised_2016.svg/1200px-Stripe_Logo%2C_revised_2016.svg.png", width=20) 
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
# 2. TODAY'S OPPORTUNITIES (HERO CARDS) & TEMPLATES (SPLIT LAYOUT)
# --------------------------------------------------
st.markdown("## Today’s Best Money Opportunities")

# Main content split: 3/4 for Data & Table, 1/4 for Outreach Panel
main_content_cols = st.columns([9, 3])

# --- LEFT COLUMN: HERO CARDS & TABLE ---
with main_content_cols[0]:
    
    # 2. HERO CARDS
    hero_cols = st.columns(3)
    
    # Helper function for colored card simulation using HTML/CSS (Simplified, tighter text)
    def render_hero_card(col, title, deal, count, color):
        with col.container(border=True, height=140): # Tighter height
            st.markdown(
                f'<div style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 14px;">{title}</div>', 
                unsafe_allow_html=True
            )
            st.markdown(f"**{deal}**", unsafe_allow_html=True) # Bold deal size
            st.markdown(f"{count} Leads Available", help="Count of leads available for this segment.")

    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", 25, COLOR_BLUE) 
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", 18, COLOR_GREEN)
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", 12, COLOR_ORANGE)

    # 5. ACTION BAR (Below Hero Cards, tighter spacing)
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    with action_buttons[0]: st.button("📥 Download CSV", key="act_csv")
    with action_buttons[1]: st.button("📊 Open in Google Sheets", key="act_sheets")
    with action_buttons[2]: st.button("✉️ Send Email", key="act_email")
    with action_buttons[3]: st.button("📞 Call", key="act_call")
    
    st.markdown("---")

    # 4. LEADS TABLE (Using native Streamlit features for clean look)
    st.markdown("### Lead Inventory (High Priority)")
    st.dataframe(
        df[["Business Name", "Phone", "Email", "Lead Score", "Reason to Contact"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            # Use progress bar for score visualization (professional and quick-read)
            "Lead Score": st.column_config.ProgressColumn("Lead Score", format="%d", min_value=0, max_value=100)
        }
    )

# --- RIGHT COLUMN: OUTREACH & EARNINGS PANEL ---
with main_content_cols[1]:
    
    # 6. OUTREACH TEMPLATES (Clean Tab Layout)
    with st.container(border=True):
        st.markdown("##### Outreach Templates")
        template_tab1, template_tab2, template_tab3 = st.tabs(["Email", "WhatsApp", "Call Scripts"])
        
        with template_tab1:
            st.caption("Subject: High-Conversion Pitch")
            st.text_area("Template", "Hi {{BusinessName}}, I noticed...", height=100, label_visibility="collapsed")
            st.button("Generate & Send", use_container_width=True, key="send_gen")

        with template_tab2:
            st.button("💬 Send WhatsApp", use_container_width=True)
            
        with template_tab3:
            st.button("📞 Start Call Script", use_container_width=True)

    # 7. POTENTIAL EARNINGS TRACKER (Clean Metric Layout)
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    with st.container(border=True):
        st.markdown("##### Potential Earnings")
        st.markdown("### Estimated Income: **$3,750 Today**")
        st.progress(70) # Progress bar showing monthly goal fulfillment
        st.caption("Contact more leads to increase earnings!")


    # 8. UPGRADE NUDGE / 9. REFERRAL ENGINE (Bottom Cards)
    st.markdown("<br>", unsafe_allow_html=True) 

    # Card 1: Unlock Premium Leads (Professional Look)
    with st.container(border=True):
        nudge_cols = st.columns([1, 2])
        with nudge_cols[0]:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/W3C_SVG_logo.svg/1200px-W3C_SVG_logo.svg.png", width=30) # Star icon placeholder
        with nudge_cols[1]:
            st.markdown("##### Unlock Premium Leads")
            st.caption("Get Exclusive High-Value Leads")
            st.button("Upgrade Now", type="primary", use_container_width=True)

    # Card 2: Earn Referral Bonuses
    with st.container(border=True):
        referral_cols = st.columns([1, 2])
        with referral_cols[0]:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/W3C_SVG_logo.svg/1200px-W3C_SVG_logo.svg.png", width=30) # Phone icon placeholder
        with referral_cols[1]:
            st.markdown("##### Earn Referral Bonuses")
            st.caption("Invite Friends & Earn Rewards")
            st.button("Invite & Earn", use_container_width=True)
