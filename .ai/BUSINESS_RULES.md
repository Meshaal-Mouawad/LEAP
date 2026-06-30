# BUSINESS_RULES.md

## Source-backed truth policy
Evidence strength: Source Code > Comments > Overrides > Governance Rules > AI Draft.

## KPI rules
Every KPI must maintain:
- Business/Metric context
- Traceability (File/Line/Logic)
- Governance status (Validated/Review Required)
- Formula derivation from code execution
- Unit of measure (if available in source)

## Governance rules
- Conflicts between business definition and code must be surfaced explicitly.
- AI must not override or certify governance status without human approval.
- Automated conflict detection for operator mismatches and variable discrepancies.
- Override ledger with SHA256 file signatures for immutable lineage tracking.

## Compliance rules
- **Saudi National Compliance:** SDAIA PDPL (privacy), NCA ECC (security), DGA (digital government).
- **International Compliance:** GDPR (data protection), SOC 2 Type II (audit), ISO 27001:2022 (security).
- **Security Rules:** Detection of injection attack vectors (os.system, eval, __import__, exec, compile).
- **Audit Rules:** Complete before/after diff and timestamp for No-Code modifications.

## Enterprise rule
Evidence must be available for all KPI explanations. No "black-box" narratives allowed.

## AI enrichment rules
- AI enrichment is optional and requires `LEAP_ENABLE_AI=1` and `OPENAI_API_KEY`.
- AI-generated content is draft-only and must be owner-validated.
- AI must not override explicit source lineage.
- Fields inferred from naming should be treated as draft evidence.

## Override rules
- Business-approved overrides stored in `kb/overrides.json` and `bluebook_generator/kb/overrides.json`.
- Overrides include SHA256 file signatures for verification.
- Overrides marked with status "APPROVED_BY_BUSINESS".
- Governance-specific overrides in `docs/governance_overrides.json`.
