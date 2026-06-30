-- KPI: Catalyst Activity Index
-- KPI: Catalyst Activity Index
SELECT active_sites / NULLIF(total_sites,0) AS [Catalyst Activity Index]
FROM (SELECT 0.87 AS active_sites, 1.0 AS total_sites) t;