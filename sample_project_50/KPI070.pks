-- KPI070: % Capacity Utilization
SELECT (SUM(actual_output) / SUM(design_capacity)) * 100 AS CapacityUtilization
FROM plants;
