# PROJECT_CONTEXT.md

## 1. Product understanding
Leap is an automated "Executable Knowledge System" that extracts KPIs and business logic from source code, validates them against governance rules, and generates narrative "Blue Book" documentation (in RST format).
- **Users:** Engineers, Business Analysts, Governance/Compliance officers.
- **Problem Solved:** Bridges the semantic disconnect between executable code and business definitions.
- **Difference:** Unlike static docs or dashboards, LEAP is evidence-based and derived directly from code execution/structure.

## 2. Research understanding
Focuses on "Executable Knowledge Systems" (PhD research). Uses static analysis (via `kpi_extractor.py`) and governance mapping to transform raw code into explainable business narratives.

## 3. Repository understanding
- **Entry Points:** `bluebook_generator/main.py`, `bluebook_generator/__main__.py`, `bluebook_generator/cli.py`, `app.py` (Flask web interface).
- **Core Modules:**
    - `bluebook_generator/kpi_extractor.py` (41KB): Source code scanner supporting 16+ file types (.py, .sql, .ps1, .dax, .cs, .vb, .abap, .st, .hdbview, .hdbprocedure, .hdbfunction, .hdbtablefunction, .sqlscript, .tsql, .pks, .pkb, .pls, .txt, .csv).
    - `bluebook_generator/governance.py` (5.6KB): Governance rule validation with automated conflict detection via `governance_patch.py`.
    - `bluebook_generator/ai_generator.py` (10KB): AI-assisted narrative drafting (optional, requires LEAP_ENABLE_AI=1 and OPENAI_API_KEY).
    - `bluebook_generator/parser.py`: Additional parsing utilities.
- **Output:** `docs/` (RST documentation generated via Sphinx with HTML build in `docs/_build/`).
- **Templates:** `templates/` (Jinja2 RST templates, HTML templates for web interface).
- **Knowledge Base:** `bluebook_generator/kb/` and `kb/` (ISO framework, KPI definitions, overrides).
- **Samples/Tests:** `sample_project/`, `sample_project_50/`, `sample_projects/leap_enterprise_scenarios/` (8 enterprise scenario KPIs), `phase3/` (ISO compliance testing).

## 4. Domain understanding
- **KPI:** A business metric embedded in code logic.
- **Extraction:** Scans files (SQL, Python, etc.) to link code to business metrics.
- **Governance:** Uses `governance_rules.json` to enforce organizational policy on discovered KPIs.

## 5. User workflows
- **CLI Developer:** Run `bluebook generate PATH/TO/SOURCE` to verify code-documentation alignment.
- **Web UI User:** Use `app.py` Flask interface for interactive KPI editing and override management.
- **Governance Reviewer:** Inspect generated RSTs/HTML for policy adherence and governance conflicts.
- **Compliance Officer:** Review automated conflict detection (operator mismatches, variable discrepancies) via governance rules.

## 6. Architecture summary
```text
Source Code Project
    ↓
bluebook_generator/kpi_extractor.py (Extraction - 16+ file types)
    ↓
bluebook_generator/governance.py (Governance/Validation + conflict detection via governance_patch.py)
    ↓
bluebook_generator/ai_generator.py (Narrative generation - optional AI enrichment)
    ↓
templates/kpi_template.rst.j2 (Jinja2 rendering)
    ↓
docs/ (RST output) → Sphinx → docs/_build/ (HTML Blue Book)
```

**Alternative Web Path:**
```text
app.py (Flask UI) → Interactive editing → Override ledger (kb/overrides.json)
```

## 7. Key files and responsibilities
| File / folder | Responsibility | Notes |
|---|---|---|
| `bluebook_generator/main.py` (100KB) | Orchestration | Monolithic; contains core pipeline logic, definition overrides, formula generation. Needs confirmation on separation of concerns. |
| `bluebook_generator/kpi_extractor.py` (41KB) | Extraction | Analyzes source files for KPI logic across 16+ file types with heuristic parsing. |
| `bluebook_generator/governance.py` (5.6KB) | Validation | Validates extracted KPIs against `governance_rules.json` and `governance_patch.py` for conflict detection. |
| `bluebook_generator/ai_generator.py` (10KB) | Narrative | AI-assisted drafting (optional, deterministic by default). |
| `bluebook_generator/cli.py` | CLI Entry | Click-based CLI with `--clean-build` and `--workers` options. |
| `app.py` (19KB) | Web UI | Flask interface for interactive KPI editing and override management. |
| `governance_patch.py` (4KB) | Conflict Logic | Evaluates logic for operator mismatches and variable discrepancies. |
| `templates/kpi_template.rst.j2` (95KB) | Rendering | Comprehensive Jinja2 template with enterprise footer and governance panels. |
| `templates/index.html` (42KB) | Web Template | Workspace interface with rich footer. |
| `docs/_templates/footer.html` (9.6KB) | Footer Partial | Shared footer component for consistency. |
| `bluebook_generator/kb/iso_framework.json` | Compliance | ISO 22400 + Saudi PDPL + NCA ECC + GDPR + SOC 2 compliance rules. |
| `docs/` | Output | RST source and HTML build (`docs/_build/`) directory. |

## 8. Current limitations
- `main.py` is overly large (100KB, 2453 lines) and likely contains mixed concerns.
- `kpi_extractor.py` uses heuristic parsing which may be brittle on complex code structures.
- Governance logic is currently tightly coupled with extraction.
- Regression testing of generated documentation is not yet automated.
- AI enrichment is optional and requires manual validation (draft-only mode).

## 9. Enterprise readiness
- **Compliance:** Enhanced with Saudi national frameworks (SDAIA PDPL, NCA ECC, DGA) and international standards (GDPR, SOC 2 Type II, ISO 27001:2022).
- **Audit Trail:** Override ledger with SHA256 file signatures for immutable lineage tracking.
- **Security:** AST input sanitization, injection attack detection (os.system, eval, __import__, exec, compile).
- **Governance:** Automated conflict detection for operator mismatches and variable discrepancies.
- **UI/UX:** Premium enterprise footer with compliance badges and responsive design.
- **Needs confirmation:** Full audit logging implementation for API calls made by `ai_generator.py`.

## 10. Open questions
- Is the current `main.py` intended to be the central monolith, or should it be decomposed? (Needs confirmation)
- Should heuristic extraction in `kpi_extractor.py` be replaced with more robust AST-based parsing? (Needs confirmation)
- What is the long-term strategy for AI enrichment validation and certification? (Needs confirmation)
