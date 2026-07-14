"""
bank_logic.py
Financing and credit-risk logic for EV battery trust scoring.
"""

import pandas as pd


RISK_BANDS = {
    "AAA": (90, 100),
    "AA":  (75, 89),
    "A":   (60, 74),
    "BBB": (45, 59),
    "BB":  (30, 44),
    "B":   (0,  29),
}


def assign_risk_band(score: float) -> str:
    """Return the credit risk band for a given health/trust score (0-100)."""
    for band, (low, high) in RISK_BANDS.items():
        if low <= score <= high:
            return band
    return "Unrated"


def compute_loan_eligibility(df: pd.DataFrame, score_col: str = "health_score") -> pd.DataFrame:
    """Add risk_band and loan_eligible columns to a DataFrame."""
    df = df.copy()
    df["risk_band"] = df[score_col].apply(assign_risk_band)
    df["loan_eligible"] = df["risk_band"].isin(["AAA", "AA", "A"])
    return df
