"""
pages/fleet_dashboard.py
Fleet overview dashboard page.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fleet Dashboard", page_icon="🚗", layout="wide")

st.title("🚗 Fleet Dashboard")
st.write("Overview of EV fleet health and charging status.")

# Placeholder — replace with real data load
st.info("Load fleet_data.csv to populate this dashboard.")
