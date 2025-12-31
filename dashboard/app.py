import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
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
    "city": "Pune",
    "niche": "Grocery Stores",
    "plan": "Pro",
    "credits": 120
}

# --------------------------------------------------
# MOCK LEADS DATA (REPLACE WITH REAL DATA PIPELINE)
# --------------------------------------------------
leads_data = [
    {
        "Business": "ABC Traders",
        "City": "Pune",
        "Niche": "Grocery",
        "Phone": "Yes",
        "Email": "Yes",
        "Reason": "No Website",
        "Score": 92
    },
    {
        "Business": "Fresh Mart",
        "City": "Pune",
        "Niche": "Grocery",
        "Phone": "Yes",
        "Email": "No",
        "Reason": "New Business",
        "Score": 85
    },
    {
        "Business": "Daily Needs",
        "City": "Pune",
        "Niche": "Grocery",
        "Phone": "Yes",
        "Email": "Yes",
        "Reason": "Poor Reviews",
        "Score": 88
    },
    {
        "Business": "Green Basket",
        "City": "Mumbai",
        "Niche": "Grocery",
        "Phone": "No",
        "Email": "Yes",
        "Reason": "No Website",
        "Score": 79
    }
]

df = pd.DataFrame(leads_data)

# --------------------------------------------------
# TOP HEADER
# --------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"### 👤 {USER['name']}")
with c2:
    st.markdown(f"📍 **City:** {USER['city']}")
with c3:
    st.markdown(f"🎯 **Niche:** {USER['niche']}")
with c4:
    st.markdown(f"💳 **Plan:** {USER['plan']}")
with c5:
    st.markdown(f"🔢 **Credits:** {USER['credits']}")

st.markdown("---")

# --------------------------------------------------
# TODAY'S OPPORTUNITIES
# --------------------------------------------------
st.markdown("## 🔥 Today’s Best Money Opportunities")

o1, o2, o3 = st.columns(3)

with o1:
    st.success("🆕 12 New Businesses\n\nEasy First Contact")
with o2:
    st.warning("📉 7 Businesses with Poor Reviews\n\nHigh Closing Chance")
with o3:
    st.info("🚀 5 High-Score Leads\n\nFast Conversion")

st.button("🚀 Start Outreach Now", use_container_width=True)

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.markdown("## 🎯 Filter Leads That Make Money")

f1, f2, f3, f4 = st.columns(4)

with f1:
    city_filter = st.selectbox("City", ["All"] + sorted(df["City"].unique().tolist()))

with f2:
    niche_filter = st.selectbox("Niche", ["All"] + sorted(df["Niche"].unique().tolist()))

with f3:
    min_score = st.slider("Minimum Lead Score", 0, 100, 70)

with f4:
    reason_filter = st.selectbox(
        "Opportunity Type",
        ["All", "No Website", "New Business", "Poor Reviews"]
    )

# Apply filters
filtered_df = df.copy()

if city_filter != "All":
    filtered_df = filtered_df[filtered_df["City"] == city_filter]

if niche_filter != "All":
    filtered_df = filtered_df[filtered_df["Niche"] == niche_filter]

if reason_filter != "All":
    filtered_df = filtered_df[filtered_df["Reason"] == reason_filter]

filtered_df = filtered_df[filtered_df["Score"] >= min_score]

# --------------------------------------------------
# LEADS TABLE
# --------------------------------------------------
st.markdown("## 📋 High Probability Leads")

st.dataframe(
    filtered_df[["Business", "City", "Phone", "Email", "Reason", "Score"]],
    use_container_width=True
)

# --------------------------------------------------
# ACTION BUTTONS
# --------------------------------------------------
a1, a2, a3, a4 = st.columns(4)

with a1:
    st.download_button(
        "📥 Download CSV",
        filtered_df.to_csv(index=False),
        file_name="leads.csv"
    )

with a2:
    st.button("📊 Open in Google Sheets")

with a3:
    st.button("✉️ Use Email Template")

with a4:
    st.button("📞 Copy Phone Numbers")

# --------------------------------------------------
# OUTREACH TOOLKIT
# --------------------------------------------------
st.markdown("## 🧰 Outreach Toolkit")

template_type = st.selectbox(
    "Select Outreach Template",
    ["Cold Call Script", "WhatsApp Message", "Email Outreach"]
)

templates = {
    "Cold Call Script": "Hi, I noticed your business is missing an online presence...",
    "WhatsApp Message": "Hello {{Business}}, I help local businesses get more customers...",
    "Email Outreach": "Subject: Grow Your Local Business\n\nHi {{Business}},\nI noticed..."
}

st.text_area("Template Preview", templates[template_type], height=120)

# --------------------------------------------------
# EARNINGS TRACKER
# --------------------------------------------------
st.markdown("## 💰 Potential Earnings Tracker")

e1, e2, e3 = st.columns(3)

with e1:
    st.metric("Leads Contacted", len(filtered_df))

with e2:
    st.metric("Estimated Close Rate", "10%")

with e3:
    potential_income = int(len(filtered_df) * 0.10 * 100)
    st.metric("Potential Income", f"${potential_income}")

# --------------------------------------------------
# UPGRADE NUDGE
# --------------------------------------------------
if USER["plan"] != "Premium":
    st.warning("🔒 Some high-score leads are locked on your plan")
    st.button("🔓 Upgrade to Premium")

# --------------------------------------------------
# REFERRAL SYSTEM
# --------------------------------------------------
st.markdown("## 🎁 Earn Free Leads")

st.info(
    "Invite friends and earn free leads:\n\n"
    "• 1 referral → 50 free leads\n"
    "• 5 referrals → 1 month Pro free"
)

st.text_input(
    "Your Referral Link",
    "https://microleadmarketplace.com/ref/ravi"
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Account")
    st.button("Profile")
    st.button("Billing")
    st.button("Logout")

    st.markdown("---")
    st.caption("© 2026 Micro Lead Marketplace")
