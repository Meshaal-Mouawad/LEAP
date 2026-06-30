AI-Powered KPI Extractor & Interactive Bluebook Generator

Step-by-step guide location: see USAGE.md in the repository root.

Quick view: After generation, open `docs/_build/index.html`.

## How it Works
- `kpi_extractor.py` scans supported source files, filters non-KPI/framework code, and keeps only candidates with KPI context plus calculation structure.
- `main.py` scopes the source evidence, generates MathJax/formula tokens from code, and renders a Jinja template.
- `ai_generator.py` is deterministic by default: it reports explicit source facts and marks missing lineage as `UNDETERMINED`.
- Optional AI enrichment is available only when deliberately enabled with `LEAP_ENABLE_AI=1` and `OPENAI_API_KEY`; AI-generated business interpretation is treated as draft text and must be owner-validated.
- Sphinx converts `.rst` into an HTML Bluebook.

## Customization
- Edit `templates/kpi_template.rst.j2` for layout.
- Add explicit `Unit:`, `Formula:`, `Objective:`, or `Data Source:` comments near KPI code when you want those fields to be certified in the Bluebook.
- Extend variable definitions in `main.generate_formula_from_code`.

## Troubleshooting
- “No KPIs found” → ensure `# KPI: Your KPI Name` is inside a function.
- Broken LaTeX → check expressions or open an issue with the example.

## Optional AI Engine
- Default mode is strict offline compliance mode.
- To enable draft AI enrichment:
  - bash `export LEAP_ENABLE_AI=1`
  - bash `export OPENAI_API_KEY=your_key`
- Optional model override:
  - bash `export LEAP_AI_MODEL=gpt-4o-mini`
- AI enrichment must not override explicit source lineage; fields inferred from naming should be treated as draft evidence.

## Example KPIs
- Overall Equipment Effectiveness (OEE)
- Ethylene Yield Percentage
- Daily Feedstock Throughput (tons/day)
- Mean Time Between Failures (hours per failure)
- Propylene to Ethylene (P/E) Ratio

## CLI usage
- Basic:
  - bash `bluebook generate path/to/your/source`
- Options:
  - `--clean-build` is retained for compatibility; generation now clears `docs/_build` before each build.
  - `--workers N` to set the number of parallel detail workers (defaults to env `KPI_AI_WORKERS` or 4)

Alternative (without installing as a script):
- bash `python -m bluebook_generator.cli generate path/to/your/source`
