-- KPI: Furnace Efficiency %
SELECT (useful_energy / NULLIF(energy_input,0)) * 100 AS [Furnace Efficiency %]
FROM (SELECT 8.2 AS useful_energy, 10.0 AS energy_input) t;