# ISO-22400 KPI Governance Test Suite

> **Purpose:** Validate LEAP AXIS ISO compliance conflict detection engine against controlled test cases.
> **Date:** 2026-06-28
> **Target Commit:** `ea2f37f` (new footer)

---

## ✅ GOAL OF THIS STEP

You want to test:

| Test Case | Expected Result |
|-----------|-----------------|
| ✅ Correct KPI | NO conflict |
| ❌ Wrong KPI (operator error) | Governance + ISO conflict |
| ❌ Wrong KPI (ISO violation) | ISO + Governance conflict |
| ❌ Non-matching KPI | NO ISO rule applied |

---

## ✅ TEST SET STRUCTURE

Create a folder:

```
test_iso_kpis/
```

---

## ✅ FILE 1 — ✅ CORRECT YIELD KPI (should PASS)

**File:** `test_iso_kpis/yield_correct.sql`

```sql
-- KPI: Yield Rate
SELECT
    (good_output_mass / raw_input_mass) * 100 AS yield_rate
FROM production_data;
```

**Expected:**
- ✅ No governance conflict
- ✅ No ISO conflict

---

## ✅ FILE 2 — ❌ WRONG YIELD (operator error)

**File:** `test_iso_kpis/yield_wrong_operator.sql`

```sql
-- KPI: Yield Rate
SELECT
    (good_output_mass + raw_input_mass) * 100 AS yield_rate
FROM production_data;
```

**Expected:**
- ⚠️ Governance Conflict
- ⚠️ ISO Conflict

**Reason:**
> Expected division (`/`)
> Found addition (`+`)

---

## ✅ FILE 3 — ❌ WRONG VARIABLES (core violation)

**File:** `test_iso_kpis/yield_wrong_variables.sql`

```sql
-- KPI: Yield Rate
SELECT
    (scrap_mass / raw_input_mass) * 100 AS yield_rate
FROM production_data;
```

**Expected:**
- ⚠️ Governance Conflict
- ⚠️ ISO Conflict

**Reason:**
> Expected `good_output_mass`
> Found `scrap_mass`

---

## ✅ FILE 4 — ✅ CORRECT UTILIZATION KPI

**File:** `test_iso_kpis/utilization_correct.sql`

```sql
-- KPI: Asset Utilization
SELECT
    actual_production_time / planned_operation_time AS utilization
FROM operations_data;
```

**Expected:**
- ✅ No ISO conflict
- ✅ No governance conflict

---

## ✅ FILE 5 — ❌ WRONG UTILIZATION KPI

**File:** `test_iso_kpis/utilization_wrong.sql`

```sql
-- KPI: Asset Utilization
SELECT
    (actual_production_time + maintenance_down_time) / planned_operation_time AS utilization
FROM operations_data;
```

**Expected:**
- ⚠️ ISO Conflict
- ⚠️ Governance Conflict

**Reason:**
> Maintenance time incorrectly included in production numerator

---

## ✅ FILE 6 — ✅ NON-ISO KPI (should NOT trigger ISO)

**File:** `test_iso_kpis/custom_kpi.sql`

```sql
-- KPI: Customer Growth Rate
SELECT
    (new_customers / total_customers) * 100 AS growth_rate
FROM crm_data;
```

**Expected:**
- ✅ NO ISO conflict
- (No template match → skipped)

---

## ✅ WHY THIS SET IS STRONG

This covers **ALL** cases:

| Case | KPI Type | Error Type | Expected Result |
|------|----------|------------|-----------------|
| 1 | `yield_efficiency` | None (correct) | ✅ Pass |
| 2 | `yield_efficiency` | Operator (`+` vs `/`) | ⚠️ ISO trigger |
| 3 | `yield_efficiency` | Variable mismatch | ⚠️ ISO trigger |
| 4 | `asset_utilization` | None (correct) | ✅ Pass |
| 5 | `asset_utilization` | Business logic error | ⚠️ ISO trigger |
| 6 | Custom (no ISO match) | N/A | ✅ Ignored |

---

## ✅ DUPLICATE KPI DEDUPLICATION (Enterprise Feature)

### Real-World Scenario

A company may have multiple files defining the same KPI:

```
yield.sql
yield_v2.sql
yield_fix.sql
yield_tmp.sql
```

All define:
```sql
-- KPI: Yield Rate
```

### What the Business Wants

✅ **ONE KPI** — NOT many duplicates

| Desired | ❌ Undesired |
|---------|-------------|
| Yield Rate ✅ | Yield Rate (v1) ❌ |
| | Yield Rate (v2) ❌ |
| | Yield Rate (temp) ❌ |

> Multiple versions confuse stakeholders and fragment governance.

### How LEAP Handles This

```
Multiple files → same KPI name → merge → keep best candidate
```

| Step | Behavior |
|------|----------|
| 1. Scan | Finds all files with `-- KPI: Yield Rate` |
| 2. Rank | Scores each candidate by confidence, explicit markers, formula quality |
| 3. Merge | Combines metadata from all sources |
| 4. Select | Keeps the **best candidate** as the canonical entry |
| 5. Report | Logs deduplication in `discovery_report.rst` |

### Why This Is Desirable

- ✅ **Single source of truth** for each KPI
- ✅ **No stakeholder confusion** from duplicate entries
- ✅ **Governance integrity** — one owner, one formula, one lineage
- ✅ **Clean Bluebook** — professional catalog without noise

### Test This Feature

Create duplicate files:

```bash
mkdir test_dedup/
```

**`test_dedup/yield_v1.sql`** (lower quality — generic comment)
```sql
-- KPI: Yield Rate
SELECT (output / input) * 100 FROM data;
```

**`test_dedup/yield_v2.sql`** (higher quality — explicit formula comment)
```sql
-- KPI: Yield Rate
-- Formula: (good_output_mass / raw_input_mass) * 100
-- Unit: %
SELECT (good_output_mass / raw_input_mass) * 100 AS yield_rate
FROM production_data;
```

**`test_dedup/yield_tmp.sql`** (lowest quality — no explicit markers)
```sql
-- KPI: Yield Rate
SELECT * FROM some_table;
```

**Expected Result:**

```
📊 Discovery Report
KPIs detected: 3 candidates
KPIs extracted: 1 (Yield Rate)

Deduplication:
  - yield_v2.sql → SELECTED (highest confidence: explicit formula + unit)
  - yield_v1.sql → MERGED (lower confidence)
  - yield_tmp.sql → FILTERED (non-KPI candidate)
```

**Verify in `docs/_build/discovery_report.html`:**
- Only **one** "Yield Rate" entry in the KPI inventory
- Confidence score reflects the best candidate (`yield_v2.sql`)
- Source lineage points to the selected file

---

## ✅ HOW TO TEST

### Run LEAP Web Interface:
```bash
python app.py
```

### Or Run CLI:
```bash
# Test ISO compliance
python bluebook_generator/cli generate test_iso_kpis/

# Test deduplication
python bluebook_generator/cli generate test_dedup/
```

---

## ✅ WHAT TO VERIFY IN OUTPUT

### Case 1 — `yield_correct.sql`
```
✅ Clean
No warning
```

### Case 2 — `yield_wrong_operator.sql`
```
⚠️ GOVERNANCE CONFLICT
⚠️ ISO Compliance Conflict
```

### Case 3 — `yield_wrong_variables.sql`
```
⚠️ ISO: variable mismatch detected
```

### Case 6 — `custom_kpi.sql`
```
✅ NO ISO alert
```

### Deduplication — `test_dedup/`
```
✅ Yield Rate (1 entry)
❌ NOT Yield Rate (v1), Yield Rate (v2), Yield Rate (temp)
```

---

## ✅ VERIFICATION CHECKLIST

### ISO Compliance Tests
- [ ] `test_iso_kpis/` folder created
- [ ] All 6 `.sql` files populated with correct content
- [ ] `kb/iso_framework.json` loaded by pipeline
- [ ] `bluebook_generator/main.py` has ISO conflict detection logic
- [ ] Run `python -m bluebook_generator.cli generate test_iso_kpis/`
- [ ] Open `docs/_build/index.html` to inspect results
- [ ] Confirm Case 1, 4, 6 show NO warnings
- [ ] Confirm Case 2, 3, 5 show ISO/Governance conflicts in sidebar

### Deduplication Tests
- [ ] `test_dedup/` folder created with 3 yield files
- [ ] Run `python -m bluebook_generator.cli generate test_dedup/`
- [ ] Open `docs/_build/discovery_report.html`
- [ ] Confirm only **1** "Yield Rate" KPI exists
- [ ] Confirm `yield_v2.sql` is the selected canonical source
- [ ] Confirm `yield_tmp.sql` is filtered as non-KPI candidate
- [ ] Verify confidence score reflects best candidate

---

## 📎 Related Files

| File | Purpose |
|------|---------|
| `kb/iso_framework.json` | ISO-22400 primitives, templates, conflict rules |
| `kb/overrides.json` | Business-approved override ledger |
| `bluebook_generator/main.py` | Extraction pipeline + ISO conflict detection |
| `bluebook_generator/parser.py` | AST mutation engine (AI-NO Mode) |
| `bluebook_generator/kpi_extractor.py` | KPI scanner + deduplication logic |
| `templates/kpi_template.rst.j2` | KPI page template with sidebar alerts |
| `docs/_static/custom.css` | Light/dark decoupled styling |

---

*Generated for LEAP AXIS Enterprise Intelligence Platform*
*Commit: `ea2f37f` — ISO-22400 Governance Framework*
