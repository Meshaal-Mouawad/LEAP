-- KPI: Aromatics Recovery %
SELECT 100 * (recovered / NULLIF(feed,0)) AS [Aromatics Recovery %]
FROM (SELECT 370 AS recovered, 400 AS feed) t;