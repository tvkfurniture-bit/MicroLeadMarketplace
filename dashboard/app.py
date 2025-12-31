# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Micro B2B Lead Marketplace",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Fake data ────────────────────────────────────────────────────────────────
leads_data = [
    {"Business Name": "BrightStar Marketing",    "Phone": "+1 555-123-4567", "Email": "info@brightstarco.com",     "Lead Score": 92,  "Reason to Contact": "New Business in Your Area"},
    {"Business Name": "GreenLeaf Cafe",           "Phone": "+1 555-234-5678", "Email": "contact@greenleafcafe.com", "Lead Score": 88,  "Reason to Contact": "No Website — Needs Online Presence"},
    {"Business Name": "Ace Fitness Center",       "Phone": "+1 555-345-6789", "Email": "info@acefitness.com",       "Lead Score": 85,  "Reason to Contact": "High Conversion Potential"},
    {"Business Name": "SwiftTech Solutions",      "Phone": "+1 555-456-7890", "Email": "sales@swifttechsol.com",    "Lead Score": 90,  "Reason to Contact": "New Startup Seeking Services"},
    {"Business Name": "Bella Boutique",           "Phone": "+1 555-567-8901", "Email": "bella@mailboutique.com",   "Lead Score": 87,  "Reason to Contact": "No Website — Expand Reach"},
]

df = pd.DataFrame(leads_data)

# ── Header / Top bar ─────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background-color:#0d1117; padding:12px; border-radius:8px; margin-bottom:1.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div style="font-size:1.4rem; font-weight:bold; color:#58a6ff;">
                <span style="color:white;">M</span> Micro B2B Lead Marketplace
            </div>
            <div style="color:#8b949e; font-size:0.95rem;">
                Welcome: <strong>John</strong> | New York, NY | Niche: Marketing Services 
                | <span style="color:#7ed957;">Pro Plan</span> | Lead Credits: <strong>85</strong>
            </div>
            <div>
                <button style="background:#238636; color:white; border:none; padding:8px 16px; border-radius:6px; margin-right:8px; cursor:pointer;">
                    Upgrade Plan
                </button>
                <button style="background:#30363d; color:#58a6ff; border:1px solid #30363d; padding:8px 16px; border-radius:6px; cursor:pointer;">
                    Refer & Earn
                </button>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ── Main Title ───────────────────────────────────────────────────────────────
st.title("Today's Best Money Opportunities")

# ── Quick opportunity cards ──────────────────────────────────────────────────
cols = st.columns([1,1,1,1.2])

with cols[0]:
    st.markdown("""
    <div style="background:#161b22; border-left:4px solid #388bfd; padding:1.2rem; border-radius:8px; margin-bottom:1rem;">
        <h4 style="margin:0; color:#388bfd;">New Businesses</h4>
        <h3 style="margin:0.4rem 0; color:#7ed957;">$500+ Potential Deal</h3>
        <p style="margin:0; color:#8b949e;">25 Leads Available</p>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div style="background:#161b22; border-left:4px solid #3fb950; padding:1.2rem; border-radius:8px; margin-bottom:1rem;">
        <h4 style="margin:0; color:#3fb950;">No Website</h4>
        <h3 style="margin:0.4rem 0; color:#7ed957;">$750+ Potential Deal</h3>
        <p style="margin:0; color:#8b949e;">18 Leads Available</p>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown("""
    <div style="background:#161b22; border-left:4px solid #f0883e; padding:1.2rem; border-radius:8px; margin-bottom:1rem;">
        <h4 style="margin:0; color:#f0883e;">High Conversion Probability</h4>
        <h3 style="margin:0.4rem 0; color:#f0883e;">$1,000+ Potential Deal</h3>
        <p style="margin:0; color:#8b949e;">12 Leads Available</p>
    </div>
    """, unsafe_allow_html=True)

with cols[3]:
    st.markdown("""
    <div style="background:#161b22; padding:1.2rem; border-radius:8px;">
        <h4 style="margin-top:0;">Outreach Templates</h4>
        <button style="background:#21262d; color:white; border:1px solid #30363d; padding:6px 12px; margin-right:6px; border-radius:6px;">Email</button>
        <button style="background:#21262d; color:white; border:1px solid #30363d; padding:6px 12px; margin-right:6px; border-radius:6px;">WhatsApp</button>
        <button style="background:#21262d; color:white; border:1px solid #30363d; padding:6px 12px; border-radius:6px;">Call Scripts</button>
    </div>
    """, unsafe_allow_html=True)

# ── Action buttons ───────────────────────────────────────────────────────────
st.markdown("---")
cols_act = st.columns([1,1,1,5])
with cols_act[0]: st.button("↓ Download CSV", use_container_width=True)
with cols_act[1]: st.button("📊 Open in Google Sheets", use_container_width=True)
with cols_act[2]: st.button("✉️ Send Email", use_container_width=True)

# ── Main leads table ─────────────────────────────────────────────────────────
st.dataframe(
    df.style.format(precision=0)
      .background_gradient(subset=["Lead Score"], cmap="YlGn")
      .highlight_max(subset=["Lead Score"], color="#2ea44f"),
    use_container_width=True,
    column_config={
        "Lead Score": st.column_config.NumberColumn("Lead Score", format="%d"),
        "Reason to Contact": st.column_config.TextColumn("Reason to Contact")
    }
)

# ── Right sidebar info ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Potential Earnings")
    st.subheader("Estimated Income: **$3,750** Today")
    
    st.progress(0.78)
    st.caption("Contact More Leads to Increase Earnings!")
    
    st.markdown("---")
    
    st.markdown("""
    ### Unlock Premium Leads
    Get Exclusive High-Value Leads
    """)
    st.button("⭐ Upgrade Now", use_container_width=True, type="primary")
    
    st.markdown("---")
    
    st.markdown("""
    ### Earn Referral Bonuses
    Invite Friends & Earn Rewards
    """)
    st.button("📲 Invite & Earn", use_container_width=True)

# ── Bottom call to action ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding:2rem; background:#161b22; border-radius:12px;">
        <h3>Want even better leads?</h3>
        <p style="color:#8b949e;">Upgrade to unlock premium, high-intent leads with $2k+ potential</p>
        <button style="background:#7ed957; color:black; font-weight:bold; padding:12px 32px; border:none; border-radius:8px; font-size:1.1rem; cursor:pointer;">
            Unlock Premium Leads Now →
        </button>
    </div>
    """,
    unsafe_allow_html=True
)
