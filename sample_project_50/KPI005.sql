-- KPI005: # Open Customer Complaints
SELECT COUNT(*)
FROM complaints
WHERE status = 'OPEN';