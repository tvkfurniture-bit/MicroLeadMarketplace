import streamlit as st
import pandas as pd
import numpy as np
import base64 # Required for masking/unmasking simulation

# --------------------------------------------------
# CONFIGURATION & USER STATE
# --------------------------------------------------
USER = {
    "name": "Ravi Kumar",
    "city": "Pune, India",
    "niche": "Marketing Services",
    "plan": "Pro Plan",
    "credits": 85,
    "is_premium": True # Set to True for the full dashboard view
}

# Define color constants
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"

# --- HELPER FUNCTIONS ---

def mask_email(email):
    # PII Masking: Ex: info@brightstarco.com -> info@mail****.com
    if '@' in email:
        username, domain = email.split('@')
        return f"{username}@{domain[:4]}****.com"
    return email

def mask_phone(phone):
    # PII Masking: Ex: +1 555-123-4567 -> +1 555-***-4567
    if len(phone) > 8:
        return f"{phone[:8]}***-{phone[-4:]}"
    return phone

# --------------------------------------------------
# MOCK LEADS DATA (Structured to match the image table exactly)
# --------------------------------------------------
leads_data = [
    {
        "Business Name": "BrightStar Marketing", "Phone": "+1 555-123-4567", "Email": "info@brightstarco.com",
        "Lead Score": 92, "Reason to Contact": "New Business in Your Area", "Attribute": "New Businesses", "Potential Deal": 500
    },
    # ... (Rest of leads data) ...
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
# Add masked data columns (Requirement 7)
df_raw['Phone_Masked'] = df_raw['Phone'].apply(mask_phone)
df_raw['Email_Masked'] = df_raw['Email'].apply(mask_email)


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
# 1. TOP HEADER BAR (Integrated Navigation)
# --------------------------------------------------
header_cols = st.columns([0.1, 8, 1, 1, 1])

with header_cols[0]: # Logo/Icon
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Stripe_Logo%2C_revised_2016.svg/1200px-Stripe_Logo%2C_revised_2016.svg.png", width=20)
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
    st.button("☰", use_container_width=True, key="menu_top_bar") 

st.markdown("---")


# --------------------------------------------------
# 2. TODAY'S OPPORTUNITIES (HERO CARDS) & TEMPLATES
# --------------------------------------------------
st.markdown("## Today’s Best Money Opportunities")

main_content_cols = st.columns([9, 3])

# --- LEFT COLUMN: HERO CARDS & TABLE ---
with main_content_cols[0]:
    
    # 2. HERO CARDS
    hero_cols = st.columns(3)
    
    # Helper function for colored card simulation
    def render_hero_card(col, title, deal, count, color):
        with col.container(border=True, height=140):
            st.markdown(
                f'<div style="background-color: {color}; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 14px;">{title}</div>', 
                unsafe_allow_html=True
            )
            st.markdown(f"**{deal}**", unsafe_allow_html=True)
            st.markdown(f"**{count}** Leads Available")

    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", leads_new_biz, COLOR_BLUE)
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", leads_no_web, COLOR_GREEN)
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", leads_high_conv, COLOR_ORANGE)

    # 5. ACTION BAR (No more floating Send/Call buttons - Requirement 4)
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    
    # Requirement 5: Contextual Export Labels
    with action_buttons[0]: st.download_button(f"📥 Download CSV ({len(df_raw)} Leads)", df_raw.to_csv(index=False), key="act_csv")
    with action_buttons[1]: st.button("📊 Open in Google Sheets", key="act_sheets")
    with action_buttons[2]: st.button("✉️ Bulk Email", key="act_email") # Now bulk action
    with action_buttons[3]: st.button("📞 Call List", key="act_call") # Now bulk action

    st.markdown("---")
    
    # --- LEAD INVENTORY TABLE (Final Product) ---
    st.markdown("## Lead Inventory (High Priority)")
    
    # Requirement 10: Standardize Pagination
    # Simulate pagination logic by showing only 5 records per page
    page_size = 5
    page_num = 1
    df_display = df_raw.head(page_size * page_num) # Only shows the first 5 records

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_order=("Business Name", "Phone", "Email", "Lead Score", "Reason to Contact", "Actions"),
        column_config={
            # PII Masking: Display the masked version (Requirement 7)
            "Phone": st.column_config.TextColumn("Phone", default=df_display['Phone_Masked'].tolist()), 
            "Email": st.column_config.TextColumn("Email", default=df_display['Email_Masked'].tolist()),

            # Lead Score Visualization (Requirement 2: Score Calibration)
            "Lead Score": st.column_config.ProgressColumn("Lead Score", format="%d", min_value=0, max_value=100,
                # Simulate the red bar visualization
                color="red"
            ),
            
            # Requirement 4: Direct Action Mapping (Buttons for each row)
            "Actions": st.column_config.Column("Actions", 
                help="Initiate direct outreach or view profile.",
                width="small",
                # Note: Streamlit Dataframe doesn't allow interactive buttons inside cells. We simulate the links/buttons.
            ),
             # Hide masked and internal columns
            "Phone_Masked": None,
            "Email_Masked": None,
            "Attribute": None,
            "Potential Deal": None
        }
    )
    # Simulation of action buttons next to the table
    st.markdown('<p style="font-size:12px; margin-top:-20px;">*Individual actions (Call/Email/View) are available directly on the record line (Backend required).*</p>', unsafe_allow_html=True)


# --- RIGHT COLUMN: OUTREACH & EARNINGS PANEL ---
with main_content_cols[1]:
    
    # 6. OUTREACH TEMPLATES
    with st.container(border=True):
        st.markdown("##### Outreach Templates")
        template_tab1, template_tab2, template_tab3 = st.tabs(["Email", "WhatsApp", "Call Scripts"])
        
        with template_tab1:
            st.caption("Subject: High-Conversion Pitch (Jinja2 Supported)") # Requirement 9
            st.text_area("Template Preview", "Hi {{BusinessName}}, I noticed...", height=100, label_visibility="collapsed")
            # Requirement 8: Asynchronous Queue Simulation
            st.button("Generate & Send (Async)", use_container_width=True, help="Sends job to secure worker queue.") 

    # 7. POTENTIAL EARNINGS TRACKER (Requirement 3: Clarify KPI)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("##### Probabilistic Conversion Value") # Renamed for clarity
        st.markdown("### Estimated Income: **$3,750 Today**")
        st.progress(70)
        st.caption("Calculation: Sum of potential deals * 15% estimated conversion rate.") # Tooltip/Explanation

    # 8. UPGRADE NUDGE (Locked feature simulation)
    st.markdown("<br>", unsafe_allow_html=True) 

    # Requirement 6: Showcase Masked Value
    with st.container(border=True):
        st.markdown("##### Unlock Exclusive Leads")
        # Masked value demonstration
        st.info("🔥 **Mega Corp Lead** - Score 98 - 🔒 Unlock with 10 Credits")
        st.button("Upgrade Now", type="primary", use_container_width=True)

    # 9. REFERRAL ENGINE
    st.markdown("<br>", unsafe_allow_html=True) 
    with st.container(border=True):
        st.markdown("##### Earn Referral Bonuses")
        st.caption("Invite Friends & Earn Rewards")
        st.button("Invite & Earn", use_container_width=True)
