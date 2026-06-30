-- KPI006: # Complaints Response Time (avg in days)
SELECT AVG(DATEDIFF(day, open_date, close_date)) AS AvgResponseTime
FROM complaints;