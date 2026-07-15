# -*- coding: utf-8 -*-
"""
modules/bank_logic.py

Converts Battery Health Score into financing decisions.
Consumes output from health_score.py — does not recalculate scores.
"""

# ---------------------------------------------------------------------------
# Remarks table
# ---------------------------------------------------------------------------
REMARKS = {
    "Approved":      "Battery condition supports standard financing.",
    "Manual Review": "Battery requires additional inspection before financing.",
    "High Risk":     "Battery health increases financing risk.",
    "Rejected":      "Battery health is below financing threshold.",
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def bank_decision(health_score: float, risk_band: str) -> dict:
    """
    Returns financing and insurance decisions based on Battery Health Score.

    Parameters
    ----------
    health_score : float  0-100  Composite score from calculate_health_score()
    risk_band    : str           Human-readable band (Excellent/Good/Moderate/Poor/Critical)

    Returns
    -------
    dict with keys:
        loan_status    (str)   Approved / Manual Review / High Risk / Rejected
        eligible       (bool)  True only when loan_status is "Approved"
        interest_rate  (str)   e.g. "8.5%" or "N/A"
        insurance_risk (str)   Low / Medium / High / Very High
        trust_level    (str)   Excellent / High / Moderate / Low / Very Low
        risk_band      (str)   Passed through from health_score output
        remarks        (str)   Human-readable explanation for the decision
    """
    # Guard — accepted values produced by health_score._risk_band()
    VALID_BANDS = {"Excellent", "Good", "Moderate", "Poor", "Critical"}
    if risk_band not in VALID_BANDS:
        raise ValueError(
            f"Invalid risk_band '{risk_band}'. "
            f"Expected one of: {sorted(VALID_BANDS)}"
        )
    if health_score >= 90:
        decision  = "Approved"
        interest  = "7.5%"
        insurance = "Low"
        trust     = "Excellent"

    elif health_score >= 75:
        decision  = "Approved"
        interest  = "8.5%"
        insurance = "Low"
        trust     = "High"

    elif health_score >= 60:
        decision  = "Manual Review"
        interest  = "10%"
        insurance = "Medium"
        trust     = "Moderate"

    elif health_score >= 40:
        decision  = "High Risk"
        interest  = "12.5%"
        insurance = "High"
        trust     = "Low"

    else:
        decision  = "Rejected"
        interest  = "N/A"
        insurance = "Very High"
        trust     = "Very Low"

    result = {
        "loan_status":    decision,
        "eligible":       decision == "Approved",
        "interest_rate":  interest,
        "insurance_risk": insurance,
        "trust_level":    trust,
        "risk_band":      risk_band,
        "remarks":        REMARKS[decision],
    }
    return result


# ---------------------------------------------------------------------------
# Quick self-test  (run: python modules/bank_logic.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_scores = [
        (95, "Excellent"),
        (82, "Good"),
        (68, "Moderate"),
        (45, "Poor"),
        (20, "Critical"),
    ]

    for score, band in test_scores:
        result = bank_decision(score, band)
        print(f"\nHealth Score: {score}  |  Band: {band}")
        print(f"  Loan Status    : {result['loan_status']}")
        print(f"  Eligible       : {result['eligible']}")
        print(f"  Interest Rate  : {result['interest_rate']}")
        print(f"  Insurance Risk : {result['insurance_risk']}")
        print(f"  Trust Level    : {result['trust_level']}")
        print(f"  Remarks        : {result['remarks']}")
