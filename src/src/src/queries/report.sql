-- Example: list top customers by total spend, including order count and last order date
SELECT
  c.customer_id,
  c.name,
  c.email,
  COUNT(DISTINCT o.order_id) AS orders_count,
  SUM(o.total_amount) AS total_spent,
  MAX(o.order_date) AS last_order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email
ORDER BY total_spent DESC
LIMIT 20;
