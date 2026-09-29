# GCP Data Platform Lab — Local Architecture

Educational mapping to Google Cloud:

| Local artifact | GCP concept |
|----------------|-------------|
| `data/bronze/` CSV landing | Cloud Storage raw bucket |
| DuckDB SQL transforms | BigQuery SQL jobs |
| `src/dags/local_medallion_dag.py` | Cloud Composer / Airflow DAG |
| `data/gold/` aggregates | BigQuery curated datasets |

No Terraform apply, no service accounts, no billing.
