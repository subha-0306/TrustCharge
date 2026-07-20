import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Config & Styles injection
# -------------------------------
from utils.ui_components import inject_master_ui, apply_plotly_theme

inject_master_ui("Manufacturer Dashboard")

# -------------------------------
# Load Live Data
# -------------------------------
try:
    df_supply = pd.read_csv("data/supply_chain.csv")
except Exception:
    df_supply = pd.DataFrame()

# -------------------------------
# Title
# -------------------------------
st.title("Manufacturer Intelligence Dashboard")
st.caption("Track material traceability, fabrication batches, supplier audit trails, and manufacturing quality controls")

st.divider()

if df_supply.empty:
    st.error("Supply chain dataset not loaded. Ensure supply_chain.csv is present in the data folder.")
else:
    # -------------------------------
    # Quality Statistics
    # -------------------------------
    total_components = len(df_supply)
    pass_rows = df_supply[df_supply["quality_check_pass"] == True]
    pass_rate = (len(pass_rows) / total_components) * 100 if total_components > 0 else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Components Traced", f"{total_components}")
    c2.metric("Quality Control Pass Rate", f"{pass_rate:.1f}%")
    c3.metric("Tracked Supplier Nodes", f"{df_supply['supplier_id'].nunique()}")

    st.divider()

    # -------------------------------
    # Grid Layout: Supply Source & Quality Distribution
    # -------------------------------
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("Material Source Origins")
        df_source = df_supply["material_source"].value_counts().reset_index()
        df_source.columns = ["Material Source", "Quantity"]
        
        fig_source = px.pie(
            df_source,
            names="Material Source",
            values="Quantity",
            hole=0.6,
            color="Material Source",
            color_discrete_sequence=["#16D9C2", "#E6A33B", "#D9534F", "#3B82F6", "#8B5CF6"],
            title="Component Materials by Origin Country"
        )
        apply_plotly_theme(fig_source)
        st.plotly_chart(fig_source, use_container_width=True)

    with right_chart:
        st.subheader("Component Quality Log Summary")
        df_pass = df_supply["quality_check_pass"].value_counts().reset_index()
        df_pass.columns = ["QC Status", "Component Count"]
        df_pass["QC Status"] = df_pass["QC Status"].map({True: "Passed Audit", False: "Flagged Defect"})

        fig_qc = px.bar(
            df_pass,
            x="QC Status",
            y="Component Count",
            color="QC Status",
            color_discrete_map={"Passed Audit": "#16D9C2", "Flagged Defect": "#D9534F"},
            title="Quality Control Pass vs Failure Comparison"
        )
        apply_plotly_theme(fig_qc)
        st.plotly_chart(fig_qc, use_container_width=True)

    st.divider()

    # -------------------------------
    # Supplier Components Logs
    # -------------------------------
    st.subheader("Component Traceability Ledger")
    st.caption("Secure blockchain-anchored ledger of cell raw component nodes")

    st.dataframe(df_supply, use_container_width=True)

st.divider()
st.caption("TrustCharge Platform Core • Dynamic Manufacturer Integration Active")
