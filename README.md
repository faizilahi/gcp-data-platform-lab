# BigQuery-Style Medallion for Subscriptions (Local SQL)

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

Local DuckDB stand-in for a BigQuery medallion serving a subscription business.
Slot debate: partition pruning on `event_date` cut scanned bytes ~**96.8%**.

## The slots argument

Unpartitioned scan of `bronze_events` estimated **12.4 GB**; partitioned path
scanned **0.4 GB** for one day — documented in `output/slots_argument.csv`.

## The partition

`event_date` daily partitions; query filters `event_date = '2024-08-21'`.

## The scheduled query

`sql/scheduled_mrr.sql` builds silver MRR. Worked MRR for 2024-08-21:
**$428,650.00** across **11,755** active subs.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_medallion.py
```
