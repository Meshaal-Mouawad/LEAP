-- KPI: Dehydrogenation Selectivity %
SELECT (desired_products / NULLIF(total_products,0)) * 100 AS [Dehydrogenation Selectivity %]
FROM (SELECT 910 AS desired_products, 1000 AS total_products) t;