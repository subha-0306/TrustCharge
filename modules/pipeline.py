# -*- coding: utf-8 -*-
"""
modules/pipeline.py

Central integration pipeline for TrustCharge.

This module coordinates:
1. RUL Prediction (Member C)
2. Readiness Score (Member D)
3. Battery Health Score (Team Lead)
4. Bank Decision Engine (Team Lead)
5. Traceability (Member D)

The Streamlit app should call ONLY:
    evaluate_vehicle(vehicle_id)
"""

try:
    # When run as a module: python -m modules.pipeline
    from modules.rul_predictor import predict_rul
    from modules.health_score import calculate_health_score
    from modules.bank_logic import bank_decision
    from modules.readiness_score import readiness_score
    from modules.trace_battery import trace_battery
except ModuleNotFoundError:
    # When run directly: python modules/pipeline.py
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from modules.rul_predictor import predict_rul
    from modules.health_score import calculate_health_score
    from modules.bank_logic import bank_decision
    from modules.readiness_score import readiness_score
    from modules.trace_battery import trace_battery

from datetime import datetime


def evaluate_vehicle(vehicle_id: str) -> dict:
    """
    Runs the complete TrustCharge evaluation pipeline.

    Parameters
    ----------
    vehicle_id : str

    Returns
    -------
    dict
        Combined result from all modules.
    """
    # ---------------------------------------------------------
    # Step 1: Get RUL prediction from Member C
    # ---------------------------------------------------------
    rul_result = predict_rul(vehicle_id)

    # ---------------------------------------------------------
    # Step 2: Readiness Score (Member D)
    # ---------------------------------------------------------
    readiness = readiness_score(vehicle_id)
    if readiness is None:
        # vehicle_id not found in fleet_routes.csv — use safe defaults
        readiness = 85

    defect_score      = 90       # placeholder — no manufacturing score source yet
    charging_score    = readiness
    temperature_score = readiness

    # ---------------------------------------------------------
    # Step 3: Calculate Battery Health Score
    # ---------------------------------------------------------
    health_result = calculate_health_score(
        rul_score=rul_result["rul_score"],
        degradation_score=rul_result["degradation_score"],
        defect_score=defect_score,
        charging_score=charging_score,
        temperature_score=temperature_score,
    )

    # ---------------------------------------------------------
    # Step 4: Get Financing Decision
    # ---------------------------------------------------------
    bank_result = bank_decision(
        health_score=health_result["health_score"],
        risk_band=health_result["risk_band"],
    )

    # ---------------------------------------------------------
    # Step 5: Traceability (Member D)
    # ---------------------------------------------------------
    # trace_battery uses battery_id — derive from vehicle_id or use first available
    battery_id = rul_result.get("vehicle_id", vehicle_id).replace("EV-", "BAT_")
    batch_id, related_batteries = trace_battery(battery_id)
    if batch_id is None:
        # Fallback: try BAT_001 as a demonstration default
        batch_id, related_batteries = trace_battery("BAT_001")

    # ---------------------------------------------------------
    # Step 6: Combine all results into one object
    # ---------------------------------------------------------
    result = {
        # Vehicle Information
        "vehicle_id":         rul_result["vehicle_id"],
        "predicted_rul_days": rul_result["predicted_rul_days"],
        "evaluation_time":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        # ML Prediction (Member C)
        "rul_prediction":     rul_result,

        # Battery Health Score (Team Lead)
        "battery_health":     health_result,

        # Financing Decision (Team Lead)
        "bank_decision":      bank_result,

        # Traceability (Member D)
        "traceability": {
            "batch_id":           batch_id,
            "related_batteries":  related_batteries,
        },
    }
    return result


# ---------------------------------------------------------
# Self-test  (run: python modules/pipeline.py)
# ---------------------------------------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path
    # Allow running directly: python modules/pipeline.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    from pprint import pprint
    result = evaluate_vehicle("EV-28EAD7C8")
    pprint(result)
