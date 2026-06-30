-- KPI007: # Number of New Customers
SELECT COUNT(*)
FROM customers
WHERE signup_date >= DATEADD(month,-1,GETDATE());