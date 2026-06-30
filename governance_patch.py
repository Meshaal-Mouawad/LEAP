import re
import json
from pathlib import Path

def _load_governance_kb():
    path = Path("phase3/kpi_governance.json")
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return []
    return []

def _load_iso_framework():
    path = Path("bluebook_generator/kb/iso_framework.json")
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return {}
    return {}

def evaluate_logic(kpi, details):
    conflicts = []
    audit_notes = []
    formula = details.get("business_formula", "")
    kpi_name = kpi.get("name", "").lower()

    # 1. Audit Notes (Missing/Incomplete Data)
    if "UNDETERMINED" in formula or not formula:
        audit_notes.append({"reason": "Business formula statement is missing or undetermined in source comments.", "severity": "Medium"})

    # 2. Potential Source Code Issues (Audit Notes)
    code = kpi.get("code_context", "")
    if re.search(r"(?i) (BUG|TODO|FIXME) ", code):
        audit_notes.append({"reason": "Found potential development issues (BUG/TODO) in source code lineage.", "severity": "Medium"})

    # 3. Governance Conflict Detection (High Severity)
    iso_kb = _load_iso_framework()
    templates = iso_kb.get("universal_metric_templates", {})
    
    matched_template = None
    expected = None  # Explicitly initialize expected
    for tmpl in templates:
        if tmpl in kpi_name:
            matched_template = tmpl
            break
            
    if matched_template:
        governance_kb = _load_governance_kb()
        expected = next(
            (item for item in governance_kb if item["kpi_name"].lower() in kpi_name),
            None
        )

    if not expected:
        return {"conflicts": [], "audit_notes": audit_notes}

    formula = details.get("business_formula", "")
    if formula:
        owner_logic = expected["roles"].get("Business Owner", "")
        if owner_logic:
            SQL_KEYWORDS = {"select", "from", "as", "and", "or"}
            
            norm_formula = re.sub(r'\s+', '', formula.lower())
            norm_owner = re.sub(r'\s+', '', owner_logic.lower())
            
            op_map = {'+': 'addition', '-': 'subtraction', '*': 'multiplication', '/': 'division'}
            
            ops_actual = set(re.findall(r'[\+\-\*/]', norm_formula))
            ops_expected = set(re.findall(r'[\+\-\*/]', norm_owner))
            
            vars_actual = {v for v in re.findall(r'\b[a-z_][a-z0-9_]*\b', norm_formula) if v not in SQL_KEYWORDS}
            vars_expected = {v for v in re.findall(r'\b[a-z_][a-z0-9_]*\b', norm_owner) if v not in SQL_KEYWORDS}
            
            operator_mismatch = (ops_actual != ops_expected)
            
            # Relaxed variable matching: structurally valid if there is at least one shared variable
            common_vars = vars_actual.intersection(vars_expected)
            missing_variables = set()
            if len(common_vars) < 1:
                missing_variables = vars_expected
            
            if operator_mismatch or missing_variables:
                conflict_reasons = []
                if operator_mismatch:
                    actual_names = [op_map.get(o, 'arithmetic') for o in ops_actual]
                    expected_names = [op_map.get(o, 'arithmetic') for o in ops_expected]
                    conflict_reasons.append(f"Operator mismatch: expected {', '.join(expected_names)} but found {', '.join(actual_names)}.")
                
                if missing_variables:
                    conflict_reasons.append(f"Incorrect variables: expected {', '.join(vars_expected)} but no shared variables found in extracted formula '{formula}'.")
                
                conflicts.append({
                    "reason": " ".join(conflict_reasons),
                    "severity": "High"
                })

    return {"conflicts": conflicts, "audit_notes": audit_notes}
