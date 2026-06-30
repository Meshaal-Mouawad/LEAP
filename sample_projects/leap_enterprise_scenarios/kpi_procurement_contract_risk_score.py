# KPI: Procurement Contract Risk Score
# Description: Combines spend leakage and urgent purchase order rate to rank procurement governance risk.
# Objective: Direct procurement leadership to business units with the highest contract compliance exposure.
# Formula: (spend_leakage_pct * 0.65) + (urgent_po_rate_pct * 0.35)
# Input: spend_leakage_pct from KPI Spend Leakage Pct and urgent_po_rate_pct from ERP purchase order workflow records.
# Unit: score
# Data Source: ERP procurement workflow records and KPI Spend Leakage Pct.
# Used In: Executive Procurement Governance Dashboard
# Comments: Synthetic test values: spend_leakage_pct=13.97 and urgent_po_rate_pct=8.25.
def procurement_contract_risk_score(
    spend_leakage_pct: float,
    urgent_po_rate_pct: float,
) -> float:
    return (spend_leakage_pct * 0.65) + (urgent_po_rate_pct * 0.35)
