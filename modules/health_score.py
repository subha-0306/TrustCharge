"""
health_score.py
Battery health scoring logic for TrustCharge.
"""

import pandas as pd
import numpy as np


def compute_health_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a normalized health score (0-100) for each battery record.

    Expected columns: soh (State of Health %), temp_c, cycle_count
    """
    df = df.copy()
    df["health_score"] = (
        0.5 * df.get("soh", 100)
        - 0.3 * (df.get("temp_c", 25) - 25).clip(lower=0)
        - 0.2 * (df.get("cycle_count", 0) / 1000)
    ).clip(0, 100).round(2)
    return df
