-- KPI003: # Justified Customer Complaints
SELECT COUNT(*) AS JustifiedComplaints
FROM complaints
WHERE justified = 1;