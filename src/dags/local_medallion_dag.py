"""
Airflow-minded DAG skeleton — runs without Airflow installed.
In GCP Composer you would schedule this graph in a managed Airflow environment.
"""
from datetime import datetime

TASKS = ["ingest_bronze", "transform_silver", "aggregate_gold"]

def run_dag():
    print(f"[DAG start] {datetime.utcnow().isoformat()}Z")
    for t in TASKS:
        print(f"  task {t}: OK (local stub)")
    print("[DAG end] invoke: python -m src.run_lab for real transforms")

if __name__ == "__main__":
    run_dag()
