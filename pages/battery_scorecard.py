import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Battery Scorecard",
    page_icon="🔋",
    layout="wide"
)

# -------------------------------
# Title
# -------------------------------
st.title("🔋 Battery Scorecard")
st.caption("Monitor battery health and performance")

st.divider()

# -------------------------------
# Vehicle Selection
# -------------------------------
vehicle = st.selectbox(
    "Select Vehicle",
    ["VEH001", "VEH002", "VEH003"]
)

# -------------------------------
# KPI Cards
# -------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Battery Health", "92%", "+2%")
c2.metric("Temperature", "31°C")
c3.metric("Voltage", "392 V")
c4.metric("RUL", "245 Days")

st.divider()

# -------------------------------
# Details + Gauge
# -------------------------------
left, right = st.columns([2,1])

with left:
    st.subheader("Battery Details")

    st.write("**Vehicle ID:**", vehicle)
    st.write("**Battery ID:** BAT001")
    st.write("**Batch ID:** BATCH007")
    st.write("**Manufacturer:** TrustCharge Energy")
    st.write("**Charge Cycles:** 185")
    st.write("**State of Charge:** 78%")
    st.write("**Health Status:** 🟢 Healthy")

with right:

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=92,
        title={"text":"Health Score"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"green"}
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------
# Degradation Trend
# -------------------------------
st.subheader("Battery Degradation Trend")

df = pd.DataFrame({
    "Month":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"],
    "Health":[100,99,98,97,96,95,94,92]
})

fig = px.line(
    df,
    x="Month",
    y="Health",
    markers=True,
    title="Battery Health Over Time"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------
# Recommendation
# -------------------------------
st.subheader("AI Recommendation")

st.success("""
Battery health is excellent.

✔ Continue normal operation.

✔ No maintenance required.

✔ Next inspection recommended after 30 days.
""")

st.divider()

# -------------------------------
# Recent Alerts
# -------------------------------
st.subheader("Recent Alerts")

alerts = pd.DataFrame({
    "Date":["10 Jul","12 Jul","14 Jul"],
    "Alert":[
        "Routine Health Check",
        "Charging Completed",
        "Battery Performing Normally"
    ]
})

st.dataframe(alerts, use_container_width=True)

st.divider()

st.caption("TrustCharge • National Level Hackathon")