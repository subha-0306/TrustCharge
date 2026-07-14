"""
utils/helpers.py
Shared utility functions for TrustCharge.
"""

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file and return a DataFrame. Returns empty DataFrame on error."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"[WARNING] File not found: {path}")
        return pd.DataFrame()


def format_score(score: float) -> str:
    """Format a 0-100 score as a colored label string."""
    if score >= 80:
        return f"🟢 {score:.1f}"
    elif score >= 50:
        return f"🟡 {score:.1f}"
    else:
        return f"🔴 {score:.1f}"
