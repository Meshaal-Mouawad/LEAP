# ARCHITECTURE.md

## Conceptual architecture
The system operates as an extraction-to-narrative pipeline:
`Source Code -> Extraction -> Semantic Structuring -> Governance -> Narrative Generation -> Blue Book`

**Alternative Web Path:**
`Source Code -> Flask UI -> Interactive Editing -> Override Ledger -> Blue Book`

## Components
| Component | Responsibility | Size |
|---|---|---|
| `cli.py` | CLI argument handling and entry point (Click-based). | 2.2KB |
| `kpi_extractor.py` | Heuristic-based static analysis to identify KPI patterns across 16+ file types. | 41KB |
| `governance.py` | Rule-based engine checking KPIs against `governance_rules.json` with conflict detection. | 5.6KB |
| `governance_patch.py` | Logic evaluation for operator mismatches and variable discrepancies. | 4KB |
| `ai_generator.py` | LLM-based narrative drafting (optional, evidence-backed, deterministic by default). | 10KB |
| `main.py` | Orchestration, definition overrides, formula generation, RST rendering. | 100KB |
| `app.py` | Flask web interface for interactive KPI editing and override management. | 19KB |
| `templates/kpi_template.rst.j2` | Jinja2 template with enterprise footer and governance panels. | 95KB |
| `templates/index.html` | Workspace interface with rich footer. | 42KB |
| `docs/_templates/footer.html` | Shared footer partial for consistency. | 9.6KB |
| `docs/` | Sphinx project structure for final rendering (RST source + HTML build). | - |

## Data-flow
### CLI Path
1. `cli.py` receives source path and options (`--clean-build`, `--workers`).
2. `kpi_extractor` scans target codebase for KPI patterns (16+ file types).
3. `governance` applies constraints from `governance_rules.json` and detects conflicts via `governance_patch.py`.
4. `ai_generator` drafts narrative (optional, requires `LEAP_ENABLE_AI=1` and `OPENAI_API_KEY`).
5. `main.py` applies definition overrides, generates formulas, renders Jinja2 templates.
6. Sphinx converts RST to HTML in `docs/_build/`.

### Web UI Path
1. `app.py` provides Flask interface for interactive editing.
2. User edits KPI definitions via web forms.
3. Changes saved to override ledger (`kb/overrides.json`) with SHA256 file signatures.
4. Override ledger applied during next generation run.

## Knowledge Base Integration
- `bluebook_generator/kb/iso_framework.json`: ISO 22400 + Saudi PDPL + NCA ECC + GDPR + SOC 2 compliance rules.
- `bluebook_generator/kb/overrides.json`: Business-approved KPI definition overrides.
- `kb/overrides.json`: Root-level override ledger.
- `docs/governance_overrides.json`: Governance-specific overrides.

## Architecture risks
- **RISK-001:** Heuristic-based extraction in `kpi_extractor.py` may be brittle on complex code structures.
- **RISK-002:** `main.py` contains monolithic orchestration (100KB, 2453 lines); risk of technical debt.
- **RISK-003:** AI enrichment requires manual validation; draft-only mode may be misinterpreted as certified.

## Recent architectural enhancements
- **Phase 3:** Logic-based heuristic detection replacing filename-reliant mechanism (reduced false positives).
- **Governance Upgrade:** Automated conflict detection for operator mismatches and variable discrepancies.
- **Compliance Upgrade:** Saudi national frameworks (SDAIA PDPL, NCA ECC, DGA) and international standards (GDPR, SOC 2 Type II, ISO 27001:2022).
- **UI/UX Upgrade:** Premium enterprise footer with compliance badges and responsive design.
- **Footer Unification:** Shared `footer.html` partial for consistency across workspace and KPI pages.

## Gemini update
The architecture is functional but needs modularization. `main.py` should be decomposed into separate orchestration and processing classes. Heuristic extraction should be evaluated for replacement with more robust AST-based parsing.
