import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np

# --------------------------------------------------
# CONFIGURATION & USER STATE (MOCK)
# --------------------------------------------------
# File Paths (Ensure these match your successful setup)
RELATIVE_LEAD_PATH = 'data/verified/verified_leads.csv'
PATHLIB_PATH = Path(__file__).parent.parent / RELATIVE_LEAD_PATH
ABSOLUTE_APP_PATH = Path("/app") / RELATIVE_LEAD_PATH

# User Data (Mimicking the latest image)
USER = {
    "name": "John", "city": "New York, NY", "niche": "Marketing Services",
    "plan": "Pro Plan", "credits": 85
}
USER_IS_PREMIUM = True # Set to True to display the full functionality shown in the final design

MAX_FREE_LEADS = 5      
SUBSCRIPTION_PRICE = 30 
TOTAL_LOCKED_LEADS = 5  

# Define color constants for the Hero Cards (Matches target image)
COLOR_BLUE = "#3b82f6"
COLOR_GREEN = "#10b981"
COLOR_ORANGE = "#f59e0b"

# --------------------------------------------------
# UTILITY: DATA LOADING AND ENRICHMENT
# --------------------------------------------------

@st.cache_data(ttl=600) 
def load_and_enrich_leads(path_1, path_2):
    try:
        # Load and clean data (Filters out INVALID_EMAIL for trust)
        df = pd.read_csv(path_1) if path_1.exists() else pd.read_csv(path_2)
        df = df[df['email'] != 'INVALID_EMAIL'].copy() 
        
        # Enrichment & Scoring (using mock logic from previous steps)
        df['city_state'] = df['address'].apply(lambda x: x.split(', ')[-2] + ', ' + x.split(', ')[-1])
        df['category'] = df.get('category', 'Uncategorized').astype(str)
        df['score'] = (df.index * 5) + 60 + pd.Series(df.index).apply(lambda x: hash(x) % 30)
        df['why_contact'] = df['email'].apply(lambda x: 'No Website – Needs Online Presence' if x.endswith('example.com') else 'New Business in Your Area')
        
        # Prepare final columns for display
        df['Phone'] = df['phone'].apply(lambda x: f"+1 {x}") 
        df['Email'] = df['email']
        df['Business Name'] = df['name']
        df['Reason to Contact'] = df['why_contact']
        df['Lead Score'] = df['score']
        
        return df.sort_values(by='Lead Score', ascending=False).reset_index(drop=True)

    except Exception as e:
        # st.error(f"Data loading error: {e}") 
        return pd.DataFrame()

df_all = load_and_enrich_leads(PATHLIB_PATH, ABSOLUTE_APP_PATH)


# --- GLOBAL PAGE CONFIG & CSS INJECTION ---
st.set_page_config(
    page_title="Micro Lead Marketplace | Dashboard",
    page_icon="Ⓜ️",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Custom CSS for Professional Density and Styling
st.markdown("""
<style>
/* Remove Streamlit default padding for header area */
.css-18e3th9 {padding-top: 0rem; padding-bottom: 0rem;}
/* Style for primary CTA button (Refer & Earn) to be red */
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #f87171 !important;
    color: white !important;
    border: none;
}
/* Style for secondary buttons (Upgrade Plan) */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: white !important;
    color: #4b5563 !important;
    border: 1px solid #d1d5db;
}
/* Hide index column from the data table */
.row_heading {display:none}
.stDataFrame { padding-top: 0px !important; }
</style>
""", unsafe_allow_html=True)


# --- TOP HEADER BAR (Integrated Navigation) ---
header_cols = st.columns([0.1, 7, 1.5, 1.5, 0.5]) 

with header_cols[0]: 
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Stripe_Logo%2C_revised_2016.svg/1200px-Stripe_Logo%2C_revised_2016.svg.png", width=20) 
with header_cols[1]: 
    st.markdown(
        f"""<p style='font-size: 13px; font-weight: 500; margin-top: 0.5rem;'>
        **Micro B2B Lead Marketplace** | Welcome: {USER['name']} | {USER['city']} | Niche: {USER['niche']} | 
        <span style='font-weight: bold;'>{USER['plan']}</span> | Lead Credits: {USER['credits']}
        </p>""", unsafe_allow_html=True
    )
with header_cols[2]:
    st.button("Upgrade Plan", use_container_width=True, key="upgrade_top", type="secondary")
with header_cols[3]:
    st.button("Refer & Earn", use_container_width=True, key="refer_top", type="primary")
with header_cols[4]:
    st.button("☰", use_container_width=True, key="menu_icon") 

st.markdown("---")


# --------------------------------------------------
# TODAY'S OPPORTUNITIES (HERO CARDS) & TEMPLATES (SPLIT LAYOUT)
# --------------------------------------------------
st.markdown("## Today’s Best Money Opportunities")

main_content_cols = st.columns([9, 3]) # 75% for Data/Table, 25% for Outreach Panel

# --- LEFT COLUMN: HERO CARDS & TABLE ---
with main_content_cols[0]:
    
    # 2. HERO CARDS LAYOUT
    hero_cols = st.columns([1, 1, 1])
    
    def render_hero_card(col, title, deal, count, color):
        with col.container(border=False):
            st.markdown(
                f"""
                <div style="background-color: {color}; color: white; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                    <p style="font-weight: bold; margin: 0; font-size: 14px;">{title}</p>
                    <h2 style="margin: 5px 0 0 0;">{deal}</h2>
                    <p style="font-size: 12px; margin: 0;">{count} Leads Available</p>
                </div>
                """, unsafe_allow_html=True
            )

    render_hero_card(hero_cols[0], "New Businesses", "$500+ Potential Deal", 25, COLOR_BLUE)
    render_hero_card(hero_cols[1], "No Website", "$750+ Potential Deal", 18, COLOR_GREEN)
    render_hero_card(hero_cols[2], "High Conversion Probability", "$1,000+ Potential Deal", 12, COLOR_ORANGE)

    # 5. ACTION BAR (Download/Sheet/Call)
    action_buttons = st.columns([1.5, 2, 1.5, 1])
    with action_buttons[0]: st.button("📥 Download CSV")
    with action_buttons[1]: st.button("📊 Open in Google Sheets")
    with action_buttons[2]: st.button("✉️ Send Email")
    with action_buttons[3]: st.button("📞 Call")
    
    st.markdown("---")

    # 4. LEADS TABLE
    st.dataframe(
        df[["Business Name", "Phone", "Email", "Lead Score", "Reason to Contact"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            # Uses Streamlit's internal styling for the progress bar look
            "Lead Score": st.column_config.ProgressColumn("Lead Score", format="%d", min_value=0, max_value=100, width="small")
        }
    )

# --- RIGHT COLUMN: OUTREACH & EARNINGS PANEL ---
with main_content_cols[1]:
    
    # 6. OUTREACH TEMPLATES (Using Tabs as in the image)
    with st.container(border=True):
        st.markdown("##### Outreach Templates")
        template_tab1, template_tab2, template_tab3 = st.tabs(["Email", "WhatsApp", "Call Scripts"])
        
        with template_tab1:
            st.text_area("Template Preview", "Subject: High-Conversion Pitch\n\nHi {{BusinessName}}, I noticed...", height=100, label_visibility="collapsed")
            st.button("Generate & Send", use_container_width=True)

    # 7. POTENTIAL EARNINGS TRACKER
    with st.container(border=True):
        st.markdown
