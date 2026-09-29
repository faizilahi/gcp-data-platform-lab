from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(428650)
rows = []
for d in pd.date_range("2024-08-01", "2024-08-31", freq="D"):
    n = 12400 if d.strftime("%Y-%m-%d") == "2024-08-21" else int(RNG.integers(11000, 13000))
    for i in range(n):
        rows.append({
            "event_date": d.strftime("%Y-%m-%d"),
            "subscription_id": f"SUB{(i % 15000):05d}",
            "status": "ACTIVE" if RNG.random() > 0.05 else "CHURNED",
            "mrr": round(float(RNG.uniform(9, 80)), 2),
            "bytes_est": 800,  # synthetic per-row byte weight
        })
df = pd.DataFrame(rows)
day = df[(df.event_date == "2024-08-21") & (df.status == "ACTIVE")].copy()
factor = 428650 / day.mrr.sum()
# scale only active that day inside full frame
mask = (df.event_date == "2024-08-21") & (df.status == "ACTIVE")
df.loc[mask, "mrr"] = (df.loc[mask, "mrr"] * factor).round(2)
drift = round(428650 - df.loc[mask, "mrr"].sum(), 2)
idx = df.loc[mask].index[-1]
df.at[idx, "mrr"] = round(df.at[idx, "mrr"] + drift, 2)
df.to_csv(DATA / "bronze_events.csv", index=False)
print("bronze", len(df))
