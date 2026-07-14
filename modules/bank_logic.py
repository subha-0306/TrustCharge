"""
modules/bank_logic.py

Financing and insurance decision engine for TrustCharge.

Public API
----------
bank_decision(health_score, risk_band) -> dict
"""

# ---------------------------------------------------------------------------
# Decision tables
# ---------------------------------------------------------------------------

# Maps risk_band -> (loan_status, interest_rate, insurance_risk)
_BAND_TABLE = {
    "AAA": ("Approved",     "7.5%",  "Very Low"),
    "AA":  ("Approved",     "8.5%",  "Low"),
    "A":   ("Approved",     "10.0%", "Low"),
    "BBB": ("Conditional",  "13.0%", "Moderate"),
    "BB":  ("Conditional",  "16.5%", "High"),
    "B":   ("Rejected",     "N/A",   "Very High"),
}

# Score thresholds for remarks
_SCORE_REMARKS = [
    (85, "Battery is in excellent condition — ideal for financing."),
    (70, "Battery is healthy and suitable for financing."),
    (55, "Battery shows moderate wear. Conditional approval recommended."),
    (40, "Battery health is below threshold. Additional inspection required."),
    (0,  "Battery is in poor condition. Financing not recommended."),
]


def _get_remark(health_score: float) -> str:
    """Return a human-readable remark based on the composite health score."""
    for threshold, remark in _SCORE_REMARKS:
        if health_score >= threshold:
            return remark
    return "Insufficient data to assess battery condition."


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def bank_decision(health_score: float, risk_band: str) -> dict:
    """
    Return a financing and insurance decision for a battery asset.

    Parameters
    ----------
    health_score : float  0–100   Composite score from calculate_health_score()
    risk_band    : str            One of: AAA, AA, A, BBB, BB, B

    Returns
    -------
    dict with keys:
        loan_status     (str)  Approved / Conditional / Rejected
        interest_rate   (str)  e.g. "8.5%" or "N/A"
        insurance_risk  (str)  Very Low / Low / Moderate / High / Very High
        remarks         (str)  Human-readable summary
    """
    band = risk_band.upper().strip()

    if band not in _BAND_TABLE:
        return {
            "loan_status":    "Rejected",
            "interest_rate":  "N/A",
            "insurance_risk": "Unknown",
            "remarks":        f"Unrecognised risk band '{risk_band}'. Cannot process application.",
        }

    loan_status, interest_rate, insurance_risk = _BAND_TABLE[band]
    remarks = _get_remark(health_score)

    return {
        "loan_status":    loan_status,
        "interest_rate":  interest_rate,
        "insurance_risk": insurance_risk,
        "remarks":        remarks,
    }


# ---------------------------------------------------------------------------
# Quick self-test  (run: python modules/bank_logic.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        {"label": "Excellent — AAA band",   "health_score": 92.0, "risk_band": "AAA"},
        {"label": "Good — AA band",         "health_score": 78.5, "risk_band": "AA"},
        {"label": "Moderate — BBB band",    "health_score": 57.0, "risk_band": "BBB"},
        {"label": "Poor — B band",          "health_score": 28.0, "risk_band": "B"},
        {"label": "Invalid band",           "health_score": 50.0, "risk_band": "ZZZ"},
    ]

    for tc in test_cases:
        result = bank_decision(tc["health_score"], tc["risk_band"])
        print(f"\n{tc['label']}")
        print(f"  Loan Status    : {result['loan_status']}")
        print(f"  Interest Rate  : {result['interest_rate']}")
        print(f"  Insurance Risk : {result['insurance_risk']}")
        print(f"  Remarks        : {result['remarks']}")
