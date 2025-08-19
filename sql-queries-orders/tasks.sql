-- Total sales volume for March 2024:
SELECT SUM(amount) AS total_sales_march_2024
FROM orders
WHERE strftime('%Y-%m', order_date) = '2024-03';

-- Customer who spent the most overall:
SELECT customer, SUM(amount) AS total_spent
FROM orders
GROUP BY customer
ORDER BY total_spent DESC
LIMIT 1;

-- Average order value for the last three months (relative to the latest order in the table):
WITH bounds AS (
  SELECT date(MAX(order_date), 'start of month') AS max_month_start
  FROM orders
),
win AS (
  SELECT date(max_month_start, '-2 months') AS from_date,
         date(max_month_start, '+1 month', '-1 day') AS to_date
  FROM bounds
)
SELECT AVG(amount) AS avg_order_value_last_3_months
FROM orders, win
WHERE order_date >= win.from_date
  AND order_date <= win.to_date;