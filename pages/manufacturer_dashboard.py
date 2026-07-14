"""
pages/manufacturer_dashboard.py
Manufacturer supply chain and trust dashboard page.
"""

import streamlit as st

st.set_page_config(page_title="Manufacturer Dashboard", page_icon="🏭", layout="wide")

st.title("🏭 Manufacturer Dashboard")
st.write("Supply chain trust scores and component quality metrics.")

st.info("Load supply_chain.csv to populate this dashboard.")
