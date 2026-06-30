-- KPI: Benzene Purity Pct
-- Description: Measures the approved benzene mass percentage from laboratory sample components.
-- Objective: Confirm that aromatics product quality is inside commercial release specification before shipment.
-- Formula: (SUM(benzene_mass_pct) / NULLIF(SUM(total_mass_pct), 0)) * 100
-- Input: benzene_mass_pct and total_mass_pct from approved LIMS sample component records.
-- Unit: %
-- Data Source: LIMS table lims_sample_components with approved chromatograph sample results.
-- Used In: Aromatics Release Readiness Index
-- Comments: Synthetic test rows represent approved analyzer samples from tank TK-204.
SELECT
    (SUM(benzene_mass_pct) / NULLIF(SUM(total_mass_pct), 0)) * 100 AS benzene_purity_pct
FROM lims_sample_components
WHERE sample_status = 'APPROVED'
  AND product_code = 'BENZENE';
