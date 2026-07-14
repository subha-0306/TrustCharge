"""
pages/battery_scorecard.py
Battery health scorecard page.
"""

import streamlit as st

st.set_page_config(page_title="Battery Scorecard", page_icon="🔋", layout="wide")

st.title("🔋 Battery Scorecard")
st.write("Detailed health scores and RUL predictions per battery unit.")

st.info("Load battery_data.csv to populate this scorecard.")
