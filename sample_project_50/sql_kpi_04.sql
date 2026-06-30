-- KPI: Hydrogen Utilization %
SELECT (consumed_h2 / NULLIF(supplied_h2,0)) * 100 AS [Hydrogen Utilization %]
FROM (
  SELECT 760 AS consumed_h2, 800 AS supplied_h2
) t;
