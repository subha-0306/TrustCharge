# -*- coding: utf-8 -*-
"""
modules/trace_battery.py

Traces a battery through the supply chain by battery_id.
Returns batch_id and all batteries in the same batch.

Integrated from Member D's Traceability Module.
Path handling updated to use pathlib (project-relative).
Tracing logic unchanged.
"""

import csv
from pathlib import Path

# Project-relative path — same pattern as rul_predictor.py
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "supply_chain.csv"


def trace_battery(battery_id):
    """
    Traces a battery by its battery_id.
    Returns its batch_id and a list of all battery_ids in that same batch.
    Handles invalid battery IDs gracefully.

    Returns
    -------
    tuple: (batch_id: str | None, related_batteries: list)
    """
    # Check if supply_chain.csv exists
    if not CSV_PATH.exists():
        print(f"Error: '{CSV_PATH}' was not found.")
        return None, []

    # Read all batteries from the supply chain CSV
    batteries = []
    with open(CSV_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            batteries.append(row)

    # Step 1: Find the batch_id for the given battery_id
    target_batch_id = None
    for item in batteries:
        if item['battery_id'] == battery_id:
            target_batch_id = item['batch_id']
            break

    # Step 2: Handle invalid battery IDs
    if target_batch_id is None:
        print(f"Warning: Battery ID '{battery_id}' was not found in supply chain database.")
        return None, []

    # Step 3: Find all other batteries in the same batch
    matching_battery_ids = []
    for item in batteries:
        if item['batch_id'] == target_batch_id:
            matching_battery_ids.append(item['battery_id'])

    return target_batch_id, matching_battery_ids


# ---------------------------------------------------------------------------
# Self-test  (run: python modules/trace_battery.py)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    print("--- Running Battery Trace Demonstration ---")

    for test_id in ["BAT_003", "BAT_006", "BAT_999"]:
        print(f"\nTracing Battery: {test_id}")
        batch, batch_list = trace_battery(test_id)
        if batch:
            print(f"  Batch ID              : {batch}")
            print(f"  Batteries in batch    : {batch_list}")
        else:
            print(f"  Result: not found in supply chain.")
