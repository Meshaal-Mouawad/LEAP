# CHANGELOG.md

## 2026-06-30 — Gemini CLI — Formula Rendering Fix
- Implemented LaTeX rendering fix in `bluebook_generator/main.py`.
- Updated `_business_formula_sentence()` to route raw LaTeX formulas through `generate_formula_from_code()`.
- Verified formula rendering via `run_generation.py`.
- Closed `RISK-007`.
