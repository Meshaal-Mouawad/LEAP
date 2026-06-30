-- KPI067: $ Fixed Cash Cost / Total Production
SELECT (SUM(fixed_cost) / SUM(total_production)) AS FixedCostPerUnit
FROM manufacturing;