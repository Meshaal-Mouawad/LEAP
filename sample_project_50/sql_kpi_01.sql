-- KPI: Ethylene Yield %
-- Compute percent yield based on good product vs total product
SELECT (good_qty * 100.0) / NULLIF(total_qty, 0) AS [Ethylene Yield %]
FROM (
  SELECT 8200 AS good_qty, 10000 AS total_qty
) t;
