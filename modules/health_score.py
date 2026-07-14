# -*- coding: utf-8 -*-
"""
modules/health_score.py

Battery health scoring engine for TrustCharge.

Public API
----------
calculate_health_score(
    rul_score,
    degradation_score,
    defect_score,
    charging_score,
    temperature_score,
) -> dict
"""

# ---------------------------------------------------------------------------
# Weights — must sum to 1.0
# Charging behaviour significantly impacts battery degradation,
# so it carries more weight than temperature stress.
# ---------------------------------------------------------------------------
WEIGHTS = {
    "rul":         0.30,   # Remaining Useful Life
    "degradation": 0.25,   # Capacity / SoH degradation
    "defect":      0.20,   # Manufacturing / physical defects
    "charging":    0.15,   # Charging pattern quality
    "temperature": 0.10,   # Thermal stress
}

assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "WEIGHTS must sum to 1.0"


# ---------------------------------------------------------------------------
# Human-readable concern labels
# ---------------------------------------------------------------------------
_CONCERN_LABELS = {
    "rul":         "Battery nearing end of life",
    "degradation": "High degradation rate",
    "defect":      "Manufacturing quality issue",
    "charging":    "Excessive fast charging",
    "temperature": "High battery temperature",
}

# ---------------------------------------------------------------------------
# Recommendation map (keyed by risk_band)
# ---------------------------------------------------------------------------
_RECOMMENDATIONS = {
    "Excellent": "Continue current maintenance schedule.",
    "Good":      "Monitor battery every month.",
    "Moderate":  "Schedule diagnostic inspection.",
    "Poor":      "Recommend preventive maintenance.",
    "Critical":  "Immediate battery replacement recommended.",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    """Clamp a value to [lo, hi]."""
    return max(lo, min(hi, value))


def _confidence(breakdown: dict) -> str:
    """
    Estimate scoring confidence based on spread of dimension scores.
    A narrow spread means all dimensions agree -> High confidence.
    A wide spread means one dimension is a strong outlier -> Medium.
    """
    spread = max(breakdown.values()) - min(breakdown.values())
    if spread < 20:
        return "High"
    elif spread < 40:
        return "Medium"
    else:
        return "Low"


def _primary_concern(scores: dict) -> str:
    """Return the human-readable label of the lowest-scoring dimension."""
    weakest_key = min(scores, key=scores.get)
    return _CONCERN_LABELS[weakest_key]


def _risk_band(health_score: float) -> str:
    """Map a 0-100 health score to a business risk band."""
    if health_score >= 90:
        return "Excellent"
    elif health_score >= 75:
        return "Good"
    elif health_score >= 60:
        return "Moderate"
    elif health_score >= 40:
        return "Poor"
    else:
        return "Critical"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def calculate_health_score(
    rul_score: float,
    degradation_score: float,
    defect_score: float,
    charging_score: float,
    temperature_score: float,
) -> dict:
    """
    Compute a weighted battery health score with business-ready insights.

    Parameters
    ----------
    rul_score         : float  0-100  Remaining Useful Life score
    degradation_score : float  0-100  Capacity / SoH degradation score
    defect_score      : float  0-100  Manufacturing / physical defect score
    charging_score    : float  0-100  Charging pattern quality score
    temperature_score : float  0-100  Thermal stress score

    Returns
    -------
    dict with keys:
        health_score     (float)  0-100 composite score, rounded to 2 dp
        risk_band        (str)    Excellent / Good / Moderate / Poor / Critical
        primary_concern  (str)    Human-readable weakest dimension
        recommendation   (str)    Actionable business recommendation
        breakdown        (dict)   Individual clamped scores per dimension
    """
    # Clamp all inputs
    breakdown = {
        "rul":         _clamp(rul_score),
        "degradation": _clamp(degradation_score),
        "defect":      _clamp(defect_score),
        "charging":    _clamp(charging_score),
        "temperature": _clamp(temperature_score),
    }

    # Weighted composite
    composite = sum(WEIGHTS[k] * v for k, v in breakdown.items())
    composite = round(_clamp(composite), 2)

    band    = _risk_band(composite)
    concern = _primary_concern(breakdown)
    recomm  = _RECOMMENDATIONS[band]
    conf    = _confidence(breakdown)

    result = {
        "health_score":    composite,
        "risk_band":       band,
        "confidence":      conf,
        "primary_concern": concern,
        "recommendation":  recomm,
        "breakdown":       breakdown,
    }
    return result


# ---------------------------------------------------------------------------
# Quick self-test  (run: python modules/health_score.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        {
            "label": "Test 1 - Healthy battery (Excellent expected)",
            "inputs": dict(rul_score=90, degradation_score=88, defect_score=95,
                           charging_score=85, temperature_score=92),
        },
        {
            "label": "Test 2 - Moderate wear (Good/Moderate expected)",
            "inputs": dict(rul_score=65, degradation_score=60, defect_score=70,
                           charging_score=55, temperature_score=68),
        },
        {
            "label": "Test 3 - Poor battery (Critical expected)",
            "inputs": dict(rul_score=25, degradation_score=30, defect_score=20,
                           charging_score=35, temperature_score=40),
        },
    ]

    for tc in test_cases:
        result = calculate_health_score(**tc["inputs"])
        print(f"\n{tc['label']}")
        print(f"  Battery Health Score : {result['health_score']}")
        print(f"  Risk Band            : {result['risk_band']}")
        print(f"  Confidence           : {result['confidence']}")
        print(f"  Primary Concern      : {result['primary_concern']}")
        print(f"  Recommendation       : {result['recommendation']}")
        print(f"  Breakdown            : {result['breakdown']}")
