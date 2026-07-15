import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Battery Scorecard",
    page_icon="🔋",
    layout="wide"
)

# -------------------------------
# Light Theme
# -------------------------------
st.markdown("""
<style>

.stApp{
    background:#F5F7FA;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:15px;
    border:1px solid #E5E7EB;
}

.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.title("🔋 Battery Health Scorecard")
st.caption("Battery health monitoring dashboard")

st.write("")

# -------------------------------
# Vehicle Selection
# -------------------------------
vehicle = st.selectbox(
    "Select Vehicle",
    ["VEH001", "VEH002", "VEH003"]
)

st.write("")

# -------------------------------
# KPI Cards
# -------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Health Score", "92%")

with c2:
    st.metric("Temperature", "31°C")

with c3:
    st.metric("Voltage", "392V")

with c4:
    st.metric("Remaining Life", "245 Days")

st.write("")
st.divider()

# -------------------------------
# Battery Details
# -------------------------------
st.subheader("Battery Information")

left,right = st.columns(2)

with left:

    st.info("""
Vehicle ID : VEH001

Battery ID : BAT001

Manufacturer : CATL

Charge Cycles : 185
""")

with right:

    st.success("""
Health Status : Excellent

Risk Band : LOW

Fast Charge Count : 5

State of Charge : 78%
""")

st.divider()

# -------------------------------
# AI Recommendation
# -------------------------------
st.subheader("AI Recommendation")

st.success("""
✅ Battery is operating normally.

• No immediate maintenance required.

• Continue regular charging schedule.

• Estimated remaining useful life is healthy.
""")

st.divider()

# -------------------------------
# Placeholder
# -------------------------------
st.markdown("""
<div style="
background:white;
padding:30px;
border-radius:15px;
border:1px solid #E5E7EB;
text-align:center;
">

<h3>📊 Live Analytics Coming Soon</h3>

<p>
Battery degradation graphs, AI predictions,
and historical trends will appear here after
backend integration.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

st.caption("TrustCharge • National Level Hackathon")