SELECT event_date,
       COUNT(DISTINCT subscription_id) AS active_subs,
       ROUND(SUM(mrr), 2) AS mrr
FROM silver_subscription_day
WHERE event_date = DATE '2024-08-21'
  AND status = 'ACTIVE'
GROUP BY 1
