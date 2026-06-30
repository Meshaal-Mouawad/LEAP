-- KPI071: % Overall Equipment Effectiveness
SELECT (Availability * Performance * Quality) * 100 AS OEE
FROM equipment_efficiency;