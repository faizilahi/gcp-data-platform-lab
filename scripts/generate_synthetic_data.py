"""Synthetic retail-style events for medallion lab (no real GCP data)."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

events = pd.DataFrame({
    "event_id": [f"E{i:04d}" for i in range(1, 121)],
    "user_id": [f"U{(i % 30) + 1:03d}" for i in range(1, 121)],
    "event_type": ["click", "purchase", "view", "add_cart"] * 30,
    "amount_usd": [round((i % 17) * 3.25, 2) for i in range(1, 121)],
    "event_ts": pd.date_range("2025-01-01", periods=120, freq="6h"),
})
events.to_csv(DATA / "raw_events.csv", index=False)

users = pd.DataFrame({
    "user_id": [f"U{i:03d}" for i in range(1, 31)],
    "country": ["US", "CA", "UK", "DE", "IN"] * 6,
    "segment": ["consumer", "pro", "enterprise"] * 10,
})
users.to_csv(DATA / "dim_users.csv", index=False)
print("Wrote raw_events.csv and dim_users.csv")
