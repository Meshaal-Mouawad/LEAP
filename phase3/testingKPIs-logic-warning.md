✅ ✅ GOAL OF THIS STEP
You want to test:
✔ Correct KPI → NO conflict
✔ Wrong KPI → Governance conflict
✔ Wrong KPI (ISO violation) → ISO + Governance conflict
✔ Non-matching KPI → NO ISO rule applied

✅ ✅ TEST SET STRUCTURE
Create a folder:
test_iso_kpis/


✅ ✅ FILE 1 — ✅ CORRECT YIELD KPI (should PASS)
yield_correct.sql

SQL-- KPI: Yield RateSELECT     (good_output_mass / raw_input_mass) * 100 AS yield_rateFROM production_data;``Show more lines

✅ Expected:
No governance conflict
No ISO conflict


✅ ✅ FILE 2 — ❌ WRONG YIELD (operator error)
yield_wrong_operator.sql

SQL-- KPI: Yield RateSELECT     (good_output_mass + raw_input_mass) * 100 AS yield_rateFROM production_data;Show more lines
✅ Expected:
Governance Conflict ✅
ISO Conflict ✅

Reason:
Expected division (/)
Found addition (+)


✅ ✅ FILE 3 — ❌ WRONG VARIABLES (core violation)
yield_wrong_variables.sql

SQL-- KPI: Yield RateSELECT     (scrap_mass / raw_input_mass) * 100 AS yield_rateFROM production_data;Show more lines
✅ Expected:
Governance Conflict ✅
ISO Conflict ✅

Reason:
Expected good_output_mass
Found scrap_mass


✅ ✅ FILE 4 — ✅ CORRECT UTILIZATION KPI
utilization_correct.sql

SQL-- KPI: Asset UtilizationSELECT     actual_production_time / planned_operation_time AS utilizationFROM operations_data;``Show more lines
✅ Expected:
No ISO conflict ✅
No governance conflict ✅


✅ ✅ FILE 5 — ❌ WRONG UTILIZATION KPI
utilization_wrong.sql

SQL-- KPI: Asset UtilizationSELECT     (actual_production_time + maintenance_down_time) / planned_operation_time AS utilizationFROM operations_data;Show more lines
✅ Expected:
ISO Conflict ✅
Governance Conflict ✅

Reason:
Maintenance time incorrectly included in production numerator


✅ ✅ FILE 6 — ✅ NON-ISO KPI (should NOT trigger ISO)
custom_kpi.sql

SQL-- KPI: Customer Growth RateSELECT     (new_customers / total_customers) * 100 AS growth_rateFROM crm_data;Show more lines
✅ Expected:
NO ISO conflict ✅
(NO template match → skipped)


✅ ✅ WHY THIS SET IS STRONG
This covers ALL cases:

































CaseExpectedCorrect KPI✅ PassOperator error✅ ISO triggerVariable mismatch✅ ISO triggerWrong business logic✅ ISO triggerDifferent KPI type✅ ignoredNormal KPI✅ pass

✅ ✅ HOW TO TEST
Run LEAP:
python app.py

OR CLI:
python bluebook_generator/cli generate test_iso_kpis/


✅ ✅ WHAT TO VERIFY IN OUTPUT

✅ Case 1 (yield_correct)
✅ Clean
No warning


✅ Case 2 (wrong operator)
⚠ GOVERNANCE CONFLICT
⚠ ISO Compliance Conflict


✅ Case 3 (wrong variable)
⚠ ISO: variable mismatch detected


✅ Case 6 (custom KPI)
NO ISO alert ✅

