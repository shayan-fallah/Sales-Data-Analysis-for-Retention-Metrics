CREATE TABLE IF NOT EXISTS customer_cohort_retention AS
WITH first_purchase AS (
  -- first purchase month for each customer
  SELECT
    customer_id,
    MIN(MONTH(transaction_date)) AS first_purchase_month
  FROM
    transactions
  GROUP BY
    customer_id
),
cohort_size AS (
  -- number of customers in each cohort (cohort size)
  SELECT
    first_purchase_month,
    COUNT(DISTINCT customer_id) AS total_customers
  FROM
    first_purchase
  GROUP BY
    first_purchase_month
)
SELECT
    fp.first_purchase_month AS cohort_month,  -- Month when the first purchase was made
    MONTH(t.transaction_date) AS activity_month,  -- Month of activity 
    COUNT(DISTINCT t.customer_id) AS retained_customers,  -- Number of customers retained in the activity month
    (COUNT(DISTINCT t.customer_id) / CAST(cs.total_customers AS FLOAT)) * 100 AS retention_rate -- Retention rate as a percentage
FROM
    transactions t
JOIN
    first_purchase fp
ON
    t.customer_id = fp.customer_id
JOIN
    cohort_size cs
ON
    fp.first_purchase_month = cs.first_purchase_month
GROUP BY
    cohort_month, activity_month, cs.total_customers
ORDER BY
    cohort_month, activity_month;
