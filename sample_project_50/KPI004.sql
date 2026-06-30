-- KPI004: # Non-Justified Customer Complaints
SELECT COUNT(*)
FROM complaints
WHERE justified = 0;