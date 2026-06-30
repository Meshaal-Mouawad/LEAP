-- KPI069: % Service Factor
SELECT (SUM(on_time_orders) / SUM(total_orders)) * 100 AS ServiceFactor
FROM orders;