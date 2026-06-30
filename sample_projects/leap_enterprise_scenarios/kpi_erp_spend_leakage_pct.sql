-- KPI: Spend Leakage Pct
-- Description: Measures the percentage of invoice spend not matched to an approved framework contract.
-- Objective: Identify procurement leakage where purchases bypass negotiated commercial agreements.
-- Formula: ((total_invoice_amt - framework_contract_amt) / NULLIF(total_invoice_amt, 0)) * 100
-- Input: total_invoice_amt and framework_contract_amt from ERP purchase ledger records.
-- Unit: %
-- Data Source: ERP procurement table erp_purchase_ledger.
-- Used In: Procurement Contract Risk Score
-- Comments: Synthetic test values: total_invoice_amt=1260000.00 and framework_contract_amt=1084000.00 for Q2.
SELECT
    ((total_invoice_amt - framework_contract_amt) / NULLIF(total_invoice_amt, 0)) * 100 AS spend_leakage_pct
FROM erp_purchase_ledger
WHERE fiscal_quarter = '2026-Q2';
