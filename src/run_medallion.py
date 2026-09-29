import json, sys
from pathlib import Path
import duckdb, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from slots import slots_argument
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA / "bronze_events.csv")
    arg = slots_argument(df, "2024-08-21")
    con = duckdb.connect()
    con.execute(f"CREATE TABLE bronze_events AS SELECT * FROM read_csv_auto('{(DATA/'bronze_events.csv').as_posix()}')")
    con.execute("""
        CREATE TABLE silver_subscription_day AS
        SELECT event_date, subscription_id, status, mrr
        FROM bronze_events
    """)
    mrr = con.execute("""
        SELECT event_date, COUNT(DISTINCT subscription_id) AS active_subs, ROUND(SUM(mrr),2) AS mrr
        FROM silver_subscription_day
        WHERE event_date = '2024-08-21' AND status = 'ACTIVE'
        GROUP BY 1
    """).df()
    mrr.to_csv(OUT / "scheduled_mrr.csv", index=False)
    pd.DataFrame([arg]).to_csv(OUT / "slots_argument.csv", index=False)
    summary = {**arg, **mrr.iloc[0].to_dict()}
    print(json.dumps(summary, indent=2, default=str))
if __name__ == "__main__":
    main()
