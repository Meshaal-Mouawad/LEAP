# LEAP_MASTER_ROADMAP.md

# Purpose

This file is the authoritative roadmap for LEAP development.
Future agents MUST use this file instead of relying on chat history.

---

# LEAP Identity

LEAP is NOT:
- documentation,
- visualization,
- reporting.

LEAP IS:
- a KPI correctness engine,
- a governance system,
- an explainable enterprise layer,
- an executable knowledge system.

---

# Phase 1 — System Foundation

## Goal
Provide a real operational platform.

## Completed
- Flask application operational
- Sphinx generation pipeline operational
- Dynamic Bluebook generation operational
- /bluebook routing fixed
- Static asset pipeline repaired
- docs/_static established as canonical asset source

## Status
✅ COMPLETE

---

# Phase 2 — KPI Discovery & Extraction

## Goal
Automatically discover KPIs from source code.

## Completed
- KPI extraction pipeline
- Confidence scoring
- Source mapping
- Formula extraction
- Lineage mapping
- Multi-file support (partial)

## Future Improvements
- Edge-case detection
- False positive reduction
- Confidence calibration

## Status
✅ COMPLETE

---

# Phase 3 — Governance & Validation

## Goal
Transform KPIs into auditable entities.

## Implemented
- Governance framework
- Review queue
- Alert framework
- KPI status system
- Evidence generation

## Planned Enhancements
- Governance conflict detection
- Formula mismatch detection
- ISO validation
- Data integrity validation
- Code drift detection
- Human override activation

## Status
🟡 LOGIC COMPLETE / ENHANCEMENT PENDING

---

# Phase 4A — UI Stability & Layout Recovery

## Goal
Deliver deterministic enterprise UI.

## Fixed
- Static asset restoration
- Missing CSS diagnosis
- Footer CSS root-cause diagnosis

## Current Regressions
- Footer visibility inconsistent
- Sidebar sections missing
- Warning panel regression
- Review queue styling regression
- Possible Sphinx layout ownership issue

## Required Sidebar Sections

- System Integrity
- Governance Scope
- Source Provenance
- Operational Actions
- Review Queue
- Extraction Method

## Success Criteria

- Footer visible on all pages
- Consistent layout across index and KPI pages
- Sidebar restored
- Missing data shown as:
    - UNDETERMINED
    - Needs Review
- Alerts only appear in sidebar
- No _build patching
- No hardcoded HTML

## Status
🚨 ACTIVE PHASE

---

# Phase 4B — Governance Intelligence

## Goal
Make LEAP governance-aware and audit-ready.

## Required Features

### Governance Conflict Detection

Detect:
- operator mismatch
- variable mismatch
- structural mismatch
- missing components

Output:

    governance_conflict=True
    conflict_reason=<deterministic explanation>
    severity=<validated|needs_review|critical>

### ISO Validation

Detect:
- ISO violations
- enterprise policy violations

### Data Integrity

Detect:
- divide by zero
- null handling
- scaling errors

### Code Drift

Track:
- code_hash

If changed:
- status=Needs Review

### Human Override

Read:
- kb/overrides.json

### Alert System

ALL alerts MUST appear ONLY in right sidebar.

## Status
⏳ LOCKED UNTIL PHASE 4A

---

# Phase 5 — Interactive Enterprise Experience

## Goal
Transform LEAP into an interactive KPI decision platform.

## Features

- KPI Knowledge Dossier
- Developer click-through to source code
- Business/developer/governance views
- Zero-code KPI creation
- Safe formula overrides
- Simulation sandbox
- Compliance boundaries

User evolution:

Viewer
→ Validator
→ Decision Maker

## Status
⏳ NOT STARTED

---

# Phase 6 — Agentic Literate Programming

## Goal

Research how AI agents understand human intent.

## Components

- .ai shared memory
- Behavioral specifications
- Agent handoffs
- Cheapkeeper Strategy Algorithm
- Shared Context Governance

## Status
🔬 RESEARCH

---

# CURRENT POSITION

Phase 1  ✅
Phase 2  ✅
Phase 3  🟡
Phase 4A 🚨 ACTIVE
Phase 4B ⏳
Phase 5  ⏳
Phase 6  🔬

---

# NEXT TASK FOR GEMINI

Read:

- .ai/START_HERE.md
- .ai/SYSTEM_BEHAVIOR_SPEC.md
- .ai/GOVERNANCE_SPEC.md
- .ai/UI_BEHAVIOR_SPEC.md
- .ai/PHASE_LOG.md
- .ai/CURRENT_STATE.md
- .ai/HANDOFF.md
- .ai/BUGS.md

Do NOT implement immediately.

First:

1. Analyze the current repository state.
2. Compare:
    - previous good KPI page
    - current generated KPI page
3. Identify all regressions introduced during UI enhancement.

Verify:

- footer visibility
- sidebar sections
- governance panels
- review queue design
- warning design
- operational actions
- source provenance
- governance scope
- layout consistency
- Sphinx wrapper ownership

Determine:

- what is complete,
- what regressed,
- what remains broken,
- exact root cause.

Only then:

- update shared memory,
- propose implementation order,
- implement Phase 4A.

Never:
- hardcode HTML,
- patch docs/_build,
- bypass Sphinx,
- remove governance,
- remove traceability,
- hide alerts.
