import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Config & Styles injection
# -------------------------------
from utils.ui_components import inject_master_ui, apply_plotly_theme

inject_master_ui("Fleet Dashboard")

# -------------------------------
# Load Live Data
# -------------------------------
try:
    df_bms = pd.read_csv("data/synthetic_bms.csv")
except Exception:
    df_bms = pd.DataFrame()

# -------------------------------
# Title
# -------------------------------
st.title("Fleet Analytics Dashboard")
st.caption("Real-time telemetry aggregation, failure anomaly detection, and fleet-wide diagnostic tracking")

st.divider()

if df_bms.empty:
    st.error("Telemetry dataset not loaded. Ensure synthetic_bms.csv is present in the data folder.")
else:
    # -------------------------------
    # Fleet Overview Stats
    # -------------------------------
    total_assets = len(df_bms)
    avg_soh = df_bms["state_of_health"].mean()
    critical_risk_count = len(df_bms[df_bms["failure_risk"] == "Critical"])
    high_risk_count = len(df_bms[df_bms["failure_risk"] == "High"])
    maint_required = len(df_bms[df_bms["maintenance_due"] == "Yes"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tracked Assets", f"{total_assets}")
    c2.metric("Fleet Average SoH", f"{avg_soh:.1f}%")
    c3.metric("Critical/High Risk Assets", f"{critical_risk_count + high_risk_count}")
    c4.metric("Pending Maintenance", f"{maint_required}")

    st.divider()

    # -------------------------------
    # Grid Layout: Risk Distribution & Cycle Degradation
    # -------------------------------
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("Fleet Risk Profile Distribution")
        df_risk_dist = df_bms["failure_risk"].value_counts().reset_index()
        df_risk_dist.columns = ["Risk Category", "Asset Count"]
        
        fig_risk = px.bar(
            df_risk_dist,
            x="Risk Category",
            y="Asset Count",
            color="Risk Category",
            color_discrete_map={
                "Low": "#16D9C2",
                "Medium": "#4E7A76",
                "High": "#E6A33B",
                "Critical": "#D9534F"
            },
            title="Battery Packs by Risk Level"
        )
        apply_plotly_theme(fig_risk)
        st.plotly_chart(fig_risk, use_container_width=True)

    with right_chart:
        st.subheader("Degradation Spread vs Charge Cycles")
        fig_cycles = px.scatter(
            df_bms,
            x="charge_cycles",
            y="state_of_health",
            color="failure_risk",
            color_discrete_map={
                "Low": "#16D9C2",
                "Medium": "#4E7A76",
                "High": "#E6A33B",
                "Critical": "#D9534F"
            },
            labels={
                "charge_cycles": "Charge Cycles Completed",
                "state_of_health": "State of Health (%)",
                "failure_risk": "Risk Level"
            },
            title="Cycle count correlation with health depletion"
        )
        apply_plotly_theme(fig_cycles)
        st.plotly_chart(fig_cycles, use_container_width=True)

    st.divider()

    # -------------------------------
    # Active Action Items: List of High Risk/Maintenance Assets
    # -------------------------------
    st.subheader("Priority Dispatch & Maintenance Action Items")
    st.caption("Battery packs currently flagged with High or Critical anomaly indicators")

    critical_df = df_bms[df_bms["failure_risk"].isin(["Critical", "High", "Medium"])][
        ["vehicle_id", "batch_id", "state_of_health", "charge_cycles", "temperature", "failure_risk", "maintenance_due"]
    ].sort_values(by="state_of_health", ascending=True)

    st.dataframe(critical_df.head(20), use_container_width=True)

    st.divider()

    # -------------------------------
    # Single Asset Lookup Mode
    # -------------------------------
    st.subheader("Individual Asset Inspector")
    selected_asset = st.selectbox(
        "Select Asset for Telemetry Inspection",
        df_bms["vehicle_id"].unique().tolist()
    )

    asset_row = df_bms[df_bms["vehicle_id"] == selected_asset].iloc[0]

    lc, rc = st.columns(2)
    with lc:
        st.info(f"""
        **Telemetry Specs:**
        - **Voltage:** `{asset_row["voltage"]:.2f} V`
        - **Operating Current:** `{asset_row["current"]:.2f} A`
        - **Internal Resistance:** `{asset_row["internal_resistance"]:.2f} mΩ`
        - **Thermal Stress Index:** `{asset_row["thermal_stress_index"]:.2f}`
        """)

    with rc:
        status_color = "Stable"
        if asset_row["failure_risk"] == "Critical":
            status_color = "Critical Anomaly Detected"
        elif asset_row["failure_risk"] == "High":
            status_color = "High Failure Risk"
        elif asset_row["failure_risk"] == "Medium":
            status_color = "Moderate Stress"

        st.success(f"""
        **Status Diagnostics:**
        - **Risk Band:** **{status_color}**
        - **RUL Remaining:** `{asset_row["rul_days"]} Days`
        - **State of Charge:** `{asset_row["state_of_charge"]:.2f}%`
        - **Maintenance Scheduled:** `{"Yes" if asset_row["maintenance_due"] == "Yes" else "No"}`
        """)

st.divider()
st.caption("TrustCharge Platform Core • Dynamic Fleet Integration Active")