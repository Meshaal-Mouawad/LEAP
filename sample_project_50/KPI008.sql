-- KPI008: % Customer Churn Rate
SELECT
    (CAST(LostCustomers AS FLOAT) / CAST(TotalCustomers AS FLOAT)) * 100 AS ChurnRate
FROM (
    SELECT COUNT(*) AS LostCustomers
    FROM customers WHERE status='Inactive'
) l, (
    SELECT COUNT(*) AS TotalCustomers
    FROM customers
) t;