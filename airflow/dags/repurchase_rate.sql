CREATE TABLE IF NOT EXISTS repurchase_rate AS
WITH customer_purchases AS (
    SELECT
        customer_id,
        COUNT(*) AS purchase_count
    FROM
        transactions
    GROUP BY
        customer_id
    HAVING
        COUNT(*) > 1
)
SELECT
    customer_id,
    (COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT customer_id) FROM transactions)) AS repurchase_rate
FROM
    customer_purchases
GROUP BY customer_id;
