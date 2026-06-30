# KPI: Aromatics Release Readiness Index
# Description: Scores whether an aromatics batch is ready for commercial release using purity and sulfur quality evidence.
# Objective: Help the quality and operations teams decide whether a tank can be released, held, or retested.
# Formula: (benzene_purity_pct * 0.75) + ((100 - sulfur_rejection_pct) * 0.25)
# Input: benzene_purity_pct from KPI Benzene Purity Pct and sulfur_rejection_pct from LIMS sulfur threshold validation.
# Unit: score
# Data Source: LIMS approved sample records and KPI Benzene Purity Pct.
# Used In: Product Release Governance Report
# Comments: Synthetic test values: benzene_purity_pct=99.71 and sulfur_rejection_pct=2.4.
def aromatics_release_readiness_index(
    benzene_purity_pct: float,
    sulfur_rejection_pct: float,
) -> float:
    return (benzene_purity_pct * 0.75) + ((100 - sulfur_rejection_pct) * 0.25)
