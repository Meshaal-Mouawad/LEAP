# BUGS.md

## Active risks

### RISK-001 — Technical Debt in `main.py`
**Status:** Open
**Severity:** Medium
**Description:** `bluebook_generator/main.py` is >100KB, indicating a likely violation of SRP.

### RISK-002 — Extraction Robustness
**Status:** Open
**Severity:** High
**Description:** `kpi_extractor.py` uses heuristic parsing which may fail on complex code structures.

### RISK-003 — AI Trustworthiness
**Status:** Open
**Severity:** High
**Description:** AI-generated narrative draft certification risk.

### RISK-005 — Missing Blue Book Static Assets
**Status:** Resolved
**Severity:** High
**Area:** Documentation
**Description:** Fixed by creating `docs/_static/` and restoring assets, and refining CSS footer visibility.

### RISK-006 — Inconsistent Footer Implementation
**Status:** Resolved
**Severity:** Low
**Area:** UI/UX
**Description:** Extracted rich footer to shared partial (`footer.html`) used by `layout.html` and `kpi_template.rst.j2`. Fixed malformed partial.

### RISK-007 — LaTeX Formula Rendering Failure
**Status:** Resolved
**Severity:** Medium
**Area:** Documentation
**Description:** Fixed by routing raw LaTeX formulas through `generate_formula_from_code()` in `_business_formula_sentence()` within `main.py`.
**Next action:** None.
