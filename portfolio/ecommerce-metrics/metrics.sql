-- SQLite SQL; synthetic sample. Completed orders only.
SELECT substr(order_date,1,7) AS month,COUNT(*) AS completed_orders,
SUM(amount_vnd) AS gmv_vnd,
ROUND(1.0*SUM(amount_vnd)/NULLIF(COUNT(*),0),2) AS aov_vnd
FROM orders WHERE status='completed'
GROUP BY substr(order_date,1,7) ORDER BY month;
SELECT category,COUNT(*) AS orders,SUM(amount_vnd) AS gmv_vnd
FROM orders WHERE status='completed' GROUP BY category ORDER BY gmv_vnd DESC;
WITH customer_orders AS (
 SELECT customer_id,COUNT(*) AS n FROM orders
 WHERE status='completed' GROUP BY customer_id
)
SELECT COUNT(*) AS customers,
SUM(CASE WHEN n>=2 THEN 1 ELSE 0 END) AS repeat_customers,
ROUND(100.0*SUM(CASE WHEN n>=2 THEN 1 ELSE 0 END)/NULLIF(COUNT(*),0),2) AS repeat_purchase_pct
FROM customer_orders;
