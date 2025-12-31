import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
# Note: Initial sidebar expanded is often needed for the initial SaaS look
st.set_page_config(
    page_title="Micro Lead Marketplace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --------------------------------------------------
# MOCK USER DATA (REPLACE LATER WITH AUTH SYSTEM)
# --------------------------------------------------
USER = {
    "name": "Ravi Kumar",
    "city": "Pune, India",
    "niche": "Grocery Stores",
    "plan": "Trial", # Set to Trial to show locked features
    "credits": 120
}

# Define color constants for the KPI cards (simulating the image)
COLOR_NEW_BUSINESS = "blue"
COLOR_NO_WEBSITE = "green"
COLOR_HIGH_CONVERSION = "orange"

# --------------------------------------------------
# MOCK LEADS DATA (REPLACE WITH REAL DATA PIPELINE)
# --------------------------------------------------
# IMPORTANT: This DataFrame structure will be enriched slightly for the table display.
leads_data = [
    {
        "Business": "BrightStar Marketing", "Phone": "+1 555-123-4567", "Email": "info@brightstarco.com",
        "Reason": "New Business in Your Area", "Score": 92, "City": "Pune", "Niche": "Grocery"
    },
    {
        "Business": "GreenLeaf Cafe", "Phone": "+1 555-234-5678", "Email": "contact@greenleafcafe.com",
        "Reason": "No Website – Needs Online Presence", "Score": 88, "City": "Pune", "Niche": "Grocery"
    },
    {
        "Business": "Ace Fitness Center", "Phone": "+1 555-345-6789", "Email": "info@acefitness.com",
        "Reason": "High Conversion Potential", "Score": 85, "City": "Mumbai", "Niche": "Hardware"
    },
    {
        "Business": "SwiftTech Solutions", "Phone": "+1 555-456-7890", "Email": "sales@swifttechsol.com",
        "Reason": "New Startup Seeking Services", "Score": 90, "City": "Pune", "Niche": "Grocery"
    },
    {
        "Business": "Bella Boutique", "Phone": "+1 555-567-8901", "Email": "bella@mailboutique.com",
        "Reason": "No Website – Expand Reach", "Score": 87, "City": "Delhi", "Niche": "Restaurants"
    }
]

df_raw = pd.DataFrame(leads_data)

# --------------------------------------------------
# TOP HEADER BAR (SaaS Style)
# --------------------------------------------------
# Simulate the horizontal top navigation (Micro B2B Lead Marketplace | Welcome: John | Plan | Refer)
header_cols = st.columns([1, 6, 1, 1, 1])

with header_cols[0]:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1200px-React-icon.svg.png", width=20) # Placeholder Icon
with header_cols[1]:
    st.markdown(
        f"**Micro B2B Lead Marketplace** | Welcome: {USER['name']} | {USER['city']} | Niche: {USER['niche']} | **{USER['plan']} Plan** | Lead Credits: {USER['credits']}",
        unsafe_allow_html=True
    )
with header_cols[2]:
    st.button("Upgrade Plan", use_container_width=True)
with header_cols[3]:
    st.button("Refer & Earn", type="primary", use_container_width=True)
with header_cols[4]:
    # Hamburger menu simulation
    st.button("☰", use_container_width=True) 

st.markdown("---")


# --------------------------------------------------
# TODAY'S OPPORTUNITIES (HERO CARDS)
# --------------------------------------------------
st.markdown("## Today’s Best Money Opportunities")

# MOCK DATA CALCULATION for the Hero Cards
leads_new_biz = len(df_raw[df_raw['Reason'].str.contains('New Business')])
leads_no_web = len(df_raw[df_raw['Reason'].str.contains('No Website')])
leads_high_conv = len(df_raw[df_raw['Score'] >= 88]) # Leads with score 88 or higher

# Split the layout: 3 Cards (70%) and 1 Outreach Panel (30%)
hero_cols = st.columns([3, 3, 3, 3])
outreach_panel = st.container()

# Card 1: New Businesses
with hero_cols[0].container(border=True, height=150):
    st.markdown(f'<div style="background-color: {COLOR_NEW_BUSINESS}; color: white; padding: 5px; border-radius: 5px;">New Businesses</div>', unsafe_allow_html=True)
    st.markdown(f"### $500+ Potential Deal")
    st.markdown(f"**{leads_new_biz}** Leads Available")

# Card 2: No Website
with hero_cols[1].container(border=True, height=150):
    st.markdown(f'<div style="background-color: {COLOR_NO_WEBSITE}; color: white; padding: 5px; border-radius: 5px;">No Website</div>', unsafe_allow_html=True)
    st.markdown(f"### $750+ Potential Deal")
    st.markdown(f"**{leads_no_web}** Leads Available")

# Card 3: High Conversion
with hero_cols[2].container(border=True, height=150):
    st.markdown(f'<div style="background-color: {COLOR_HIGH_CONVERSION}; color: white; padding: 5px; border-radius: 5px;">High Conversion Probability</div>', unsafe_allow_html=True)
    st.markdown(f"### $1,000+ Potential Deal")
    st.markdown(f"**{leads_high_conv}** Leads Available")

# 4. OUTREACH TOOLKIT (Right Panel Simulation)
with hero_cols[3]:
    st.markdown("##### Outreach Templates")
    template_tab1, template_tab2, template_tab3 = st.tabs(["Email", "WhatsApp", "Call Scripts"])
    
    with template_tab1:
        st.caption("Subject: High-Conversion Pitch")
        st.button("✉️ Send Email", use_container_width=True)

    with template_tab2:
        st.button("💬 Send WhatsApp", use_container_width=True)
        
    with template_tab3:
        st.button("📞 Start Call", use_container_width=True)
    
    # Potential Earnings (Small card simulation)
    st.markdown("##### Potential Earnings")
    st.metric("Estimated Income", "$3,750 Today", delta="Contact more leads to increase earnings!")


# --------------------------------------------------
# ACTION BAR (Download/Sheet/Call)
# --------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Note: Using st.columns for clean spacing below the cards
action_buttons = st.columns(4)

with action_buttons[0]:
    st.download_button(
        "📥 Download CSV",
        df_raw.to_csv(index=False),
        file_name="leads.csv"
    )

with action_buttons[1]:
    st.button("📊 Open in Google Sheets")

with action_buttons[2]:
    st.button("✉️ Send Email") # Unified button leading to the right panel
    
with action_buttons[3]:
    st.button("📞 Call")


# --------------------------------------------------
# DATA SEGMENTATION & LEADS TABLE (3 & 4)
# --------------------------------------------------
st.markdown("## Filter Leads & Inventory")

# Combined Filters and Table into one segment
filter_and_table = st.columns([1, 4])

with filter_and_table[0]:
    # Filter controls placed compactly on the left (simulating filter panel)
    st.markdown("##### Segmentation Controls")
    city_filter = st.selectbox("City", ["All"] + sorted(df_raw["City"].unique().tolist()), label_visibility="collapsed", index=0)
    niche_filter = st.selectbox("Niche", ["All"] + sorted(df_raw["Niche"].unique().tolist()), label_visibility="collapsed")
    min_score = st.slider("Min Score", 0, 100, 70, label_visibility="collapsed")
    reason_filter = st.selectbox("Type", ["All", "No Website", "New Business", "Poor Reviews"], label_visibility="collapsed")
    st.button("Apply Segmentation", use_container_width=True)
    
    # 8. UPGRADE NUDGE (Locked feature simulation)
    st.markdown("---")
    st.markdown("##### Unlock Premium Leads")
    st.info("Get exclusive high-value leads.")
    st.button("Upgrade Now", use_container_width=True)

with filter_and_table[1]:
    # Apply filters (Functional philosophy logic)
    filtered_df = df_raw.copy()
    if city_filter != "All":
        filtered_df = filtered_df[filtered_df["City"] == city_filter]
    # ... (Other filter logic would go here)
    filtered_df = filtered_df[filtered_df["Score"] >= min_score]

    st.markdown("##### Lead Inventory (High Priority)")
    
    # Filter the table display to match the required columns
    display_df = filtered_df[["Business", "Phone", "Email", "Score", "Reason"]].rename(
        columns={
            "Score": "Lead Score",
            "Reason": "Reason to Contact"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        # Use HTML/CSS injection via Streamlit Component or Markdown if further styling is needed
    )

# 9. REFERRAL ENGINE (Bottom Card)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## Referral Engine")
referral_cols = st.columns([2, 8])

with referral_cols[0].container(border=True, height=100):
    st.markdown("##### Earn Referral Bonuses")
    st.caption("Invite friends & earn rewards.")

with referral_cols[1]:
    st.info(
        "Invite 1 friend → Get 50 free leads\n\n"
        "Invite 5 friends → 1 Month Pro Free"
    )
    st.text_input("Your Referral Link", "https://microleadmarketplace.com/ref/ravi", disabled=True)
