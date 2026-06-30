# Governance Conflict Detection Upgrade

Implemented automated governance conflict detection by comparing extracted KPI formulas against a Knowledge Base (`kpi_governance.json`).

## Enhancements
- Added `evaluate_logic` logic in `governance_patch.py`.
- Automated detection of:
  - **Operator Mismatches:** Detects arithmetic differences (e.g. `+` vs `/`).
  - **Variable Discrepancies:** Identifies missing required logic components.
  - **Severity Scoring:** categorizes issues as Medium or High depending on the nature of the conflict.
- Integration: The `infer_raci` function in `governance.py` now populates `raci['conflicts']` dynamically.
