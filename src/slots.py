import pandas as pd

def slots_argument(df: pd.DataFrame, day: str) -> dict:
    full_bytes = int(df["bytes_est"].sum())
    part_bytes = int(df.loc[df["event_date"] == day, "bytes_est"].sum())
    # scale to teaching GB numbers
    scale = 12.4e9 / full_bytes
    full_gb = round(full_bytes * scale / 1e9, 1)
    part_gb = round(part_bytes * scale / 1e9, 1)
    return {
        "unpartitioned_scan_gb": full_gb,
        "partitioned_scan_gb": part_gb,
        "reduction_pct": round((1 - part_gb / full_gb) * 100, 1),
    }
