-- KPI066: $ Variable Cost / Total Production
SELECT (SUM(variable_cost) / SUM(total_production)) AS VarCostPerUnit
FROM manufacturing;