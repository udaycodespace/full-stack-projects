-- Monthly revenue aggregated by month
WITH revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        SUM(o.amount) AS gross_revenue
    FROM orders o
    WHERE o.status = 'completed'
    GROUP BY 1
)
SELECT
    month,
    gross_revenue,
    ROW_NUMBER() OVER (ORDER BY month) AS month_rank
FROM revenue
ORDER BY month;

-- Top customers by lifetime spend
WITH customer_totals AS (
    SELECT
        c.customer_id,
        c.name,
        COUNT(o.order_id) AS order_count,
        SUM(o.amount) AS lifetime_revenue
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
    GROUP BY c.customer_id
)
SELECT
    customer_id,
    name,
    order_count,
    lifetime_revenue
FROM customer_totals
ORDER BY lifetime_revenue DESC NULLS LAST
LIMIT 20;

-- Validation: Negative or zero-dollar orders
SELECT
    order_id,
    customer_id,
    amount,
    status,
    order_date
FROM orders
WHERE amount <= 0
ORDER BY order_date DESC;

-- Validation: Failed payments and their orders
SELECT
    p.payment_id,
    p.order_id,
    o.customer_id,
    p.gateway,
    p.amount,
    p.failure_code,
    p.payment_date
FROM payments p
LEFT JOIN orders o ON o.order_id = p.order_id
WHERE p.success = FALSE
ORDER BY p.payment_date DESC;
