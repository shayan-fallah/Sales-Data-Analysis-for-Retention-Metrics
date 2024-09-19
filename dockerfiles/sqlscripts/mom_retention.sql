CREATE TABLE IF NOT EXISTS monthly_customer_retention AS
SELECT
    MONTH(t1.transaction_date) AS current_month,
    COUNT(DISTINCT t1.customer_id) AS total_customers_in_current_month,
    COUNT(DISTINCT t2.customer_id) AS retained_customers_from_previous_month,
    (COUNT(DISTINCT t2.customer_id) / COUNT(DISTINCT t1.customer_id)) * 100 AS retention_rate
FROM
    transactions t1
LEFT JOIN
    transactions t2
ON
    t1.customer_id = t2.customer_id
    AND MONTH(t2.transaction_date) = MONTH(t1.transaction_date) - 1
    AND YEAR(t2.transaction_date) = YEAR(t1.transaction_date)
GROUP BY
    current_month
ORDER BY
    current_month;
