"""
fake_pipeline.py
Generates synthetic EV charging station data using Faker.
"""

import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()


def generate_stations(n: int = 100) -> pd.DataFrame:
    """Generate n fake EV charging stations."""
    records = []
    for _ in range(n):
        records.append({
            "station_id": fake.uuid4(),
            "name": f"{fake.company()} Charging Hub",
            "city": fake.city(),
            "state": fake.state(),
            "latitude": float(fake.latitude()),
            "longitude": float(fake.longitude()),
            "charger_type": np.random.choice(["Level 1", "Level 2", "DC Fast"]),
            "trust_score": round(np.random.uniform(0, 1), 3),
            "uptime_pct": round(np.random.uniform(70, 100), 2),
            "avg_rating": round(np.random.uniform(1, 5), 2),
        })
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_stations(10)
    print(df.head())
