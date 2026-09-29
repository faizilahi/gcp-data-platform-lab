"""Run bronze → silver → gold with DuckDB (BigQuery-style SQL locally)."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
BRONZE = ROOT / "data" / "bronze"
SILVER = ROOT / "data" / "silver"
GOLD = ROOT / "data" / "gold"
for p in (BRONZE, SILVER, GOLD):
    p.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(ROOT / "warehouse.duckdb"))
con.execute("CREATE OR REPLACE TABLE bronze_events AS SELECT * FROM read_csv_auto(?)", [str(ROOT / "data" / "raw_events.csv")])
con.execute("""
CREATE OR REPLACE TABLE silver_events AS
SELECT e.*, u.country, u.segment
FROM bronze_events e
LEFT JOIN read_csv_auto(?) u ON e.user_id = u.user_id
WHERE e.amount_usd >= 0
""", [str(ROOT / "data" / "dim_users.csv")])
con.execute("""
CREATE OR REPLACE TABLE gold_daily_revenue AS
SELECT CAST(event_ts AS DATE) AS day, SUM(amount_usd) AS revenue_usd, COUNT(*) AS events
FROM silver_events
GROUP BY 1 ORDER BY 1
""")
con.execute(f"COPY bronze_events TO '{BRONZE / 'events.parquet'}' (FORMAT PARQUET)")
con.execute(f"COPY silver_events TO '{SILVER / 'events_enriched.parquet'}' (FORMAT PARQUET)")
con.execute(f"COPY gold_daily_revenue TO '{GOLD / 'daily_revenue.parquet'}' (FORMAT PARQUET)")
print(con.execute("SELECT * FROM gold_daily_revenue LIMIT 5").fetchdf())
print("Pipeline complete. Parquet layers written under data/bronze|silver|gold.")
