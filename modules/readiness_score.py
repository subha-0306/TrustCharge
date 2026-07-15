# -*- coding: utf-8 -*-
"""
modules/readiness_score.py

Calculates operational readiness score (0-100) for a vehicle
based on fleet route characteristics.

Integrated from Member D's Traceability Module.
Path handling updated to use pathlib (project-relative).
Scoring logic unchanged.
"""

import csv
from pathlib import Path

# Project-relative path — same pattern as rul_predictor.py
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "fleet_routes.csv"


def readiness_score(vehicle_id):
    """
    Calculates the readiness score (0-100) for a given vehicle_id.
    Reads data from data/fleet_routes.csv and applies rule-based logic.
    """
    # Check if the CSV file exists
    if not CSV_PATH.exists():
        print(f"Error: '{CSV_PATH}' was not found.")
        return None

    # Open and read the CSV file
    with open(CSV_PATH, mode='r') as file:
        reader = csv.DictReader(file)

        vehicle_data = None
        for row in reader:
            if row['vehicle_id'] == vehicle_id:
                vehicle_data = row
                break

        # If the vehicle_id was not found in the CSV, return None
        if not vehicle_data:
            print(f"Vehicle '{vehicle_id}' not found in fleet_routes database.")
            return None

    # Convert values from string to float
    daily_distance       = float(vehicle_data['daily_distance'])
    payload              = float(vehicle_data['payload'])
    dwell_time           = float(vehicle_data['dwell_time'])
    route_predictability = float(vehicle_data['route_predictability'])

    # --- RULE-BASED SCORING FORMULA (unchanged) ---
    score = 100

    # 1. Distance Penalty
    if daily_distance <= 100:
        distance_penalty = 0
    elif daily_distance <= 250:
        distance_penalty = 15
    else:
        distance_penalty = 30

    # 2. Payload Penalty
    if payload <= 500:
        payload_penalty = 0
    elif payload <= 1500:
        payload_penalty = 10
    else:
        payload_penalty = 20

    # 3. Dwell Time Penalty
    if dwell_time >= 5:
        dwell_penalty = 0
    elif dwell_time >= 2:
        dwell_penalty = 15
    else:
        dwell_penalty = 30

    # 4. Predictability Penalty
    if route_predictability >= 0.9:
        predictability_penalty = 0
    elif route_predictability >= 0.7:
        predictability_penalty = 10
    else:
        predictability_penalty = 20

    final_score = score - distance_penalty - payload_penalty - dwell_penalty - predictability_penalty
    final_score = max(0, min(100, final_score))

    return final_score


# ---------------------------------------------------------------------------
# Self-test  (run: python modules/readiness_score.py)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    print("--- Calculating Readiness Scores for EV Fleet ---")
    test_vehicles = ["EV_001", "EV_002", "EV_003", "EV_004", "EV_005", "EV_999"]

    for v_id in test_vehicles:
        score = readiness_score(v_id)
        if score is not None:
            print(f"Vehicle: {v_id} | Readiness Score: {score}/100")
