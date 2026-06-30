#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "sample_project_50"
OUT.mkdir(parents=True, exist_ok=True)

# Utilities


def w(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---- Templates per language ----


def sql_file(name: str, alias: str, expr: str) -> str:
    return (
        f"""-- KPI: {name}\nSELECT {expr} AS [{alias}]\nFROM (SELECT 1 AS dummy) t;\n"""
    )


def tsql_file(name: str, alias: str, expr: str) -> str:
    return f"""-- KPI: {name}\nSELECT {expr} AS [{alias}]\nGO\n"""


def plsql_spec(name: str, func: str) -> str:
    return f"""-- KPI: {name}\nCREATE OR REPLACE PACKAGE {func}_pkg AS\n  FUNCTION {func} RETURN NUMBER;\nEND {func}_pkg;\n/\n"""


def plsql_body(name: str, func: str, expr: str) -> str:
    return f"""-- KPI: {name}\nCREATE OR REPLACE PACKAGE BODY {func}_pkg AS\n  FUNCTION {func} RETURN NUMBER IS\n    a NUMBER := 910;\n    b NUMBER := 1000;\n    r NUMBER;\n  BEGIN\n    r := {expr};\n    RETURN r;\n  END {func};\nEND {func}_pkg;\n/\n"""


def hana_view(name: str, alias: str, expr: str) -> str:
    return f"""-- KPI: {name}\nSELECT {expr} AS \"{alias}\" FROM DUMMY;\n"""


def python_file(name: str, expr: str) -> str:
    return f"""# KPI: {name}\n\ndef calc():\n    good = 8200.0\n    total = 10000.0\n    result = {expr}\n    return result\n\nif __name__ == "__main__":\n    print(calc())\n"""


def dax_file(name: str, expr: str) -> str:
    return f"""-- KPI: {name}\n{name} = {expr}\n"""


def cs_file(name: str, expr: str) -> str:
    return f"""// KPI: {name}\npublic class Kpi {{\n    public double Calc() {{\n        double a = 8200, b = 10000;\n        double result = {expr};\n        return result;\n    }}\n}}\n"""


def vb_file(name: str, expr: str) -> str:
    return f"""' KPI: {name}\nModule Kpi\n  Function Calc() As Double\n    Dim a As Double = 8200\n    Dim b As Double = 10000\n    Dim result As Double = {expr}\n    Return result\n  End Function\nEnd Module\n"""


def abap_file(name: str, expr: str) -> str:
    return f"""* KPI: {name}\nDATA: a TYPE f VALUE '8200', b TYPE f VALUE '10000', res TYPE f.\nres = {expr}.\nWRITE res.\n"""


def st_file(name: str, expr: str) -> str:
    return f"""(* KPI: {name} *)\nVAR\n    a : REAL := 8200.0;\n    b : REAL := 10000.0;\n    result : REAL;\nEND_VAR\nresult := {expr};\n"""


# ---- Plan: create 50 files in the agreed distribution ----

sql_items = [
    ("Ethylene Yield %", "Ethylene Yield %", "(8200.0 * 100.0) / NULLIF(10000.0,0)"),
    ("Propylene Yield %", "Propylene Yield %", "100.0 * (4500.0 / NULLIF(5200.0,0))"),
    (
        "Polymerization Conversion %",
        "Polymerization Conversion %",
        "(980.0 / NULLIF(1000.0,0)) * 100",
    ),
    (
        "Hydrogen Utilization %",
        "Hydrogen Utilization %",
        "(760.0 / NULLIF(800.0,0)) * 100",
    ),
    ("Aromatics Recovery %", "Aromatics Recovery %", "100 * (370.0 / NULLIF(400.0,0))"),
    (
        "Dehydrogenation Selectivity %",
        "Dehydrogenation Selectivity %",
        "(910.0 / NULLIF(1000.0,0)) * 100",
    ),
    ("Catalyst Activity Index", "Catalyst Activity Index", "0.87 / NULLIF(1.0,0)"),
    ("Furnace Efficiency %", "Furnace Efficiency %", "(8.2 / NULLIF(10.0,0)) * 100"),
]

# Write SQL files
for i, (n, a, e) in enumerate(sql_items, start=1):
    w(OUT / f"sql_kpi_{i:02d}.sql", sql_file(n, a, e))

# T-SQL 6
tsql_items = [
    ("Benzene Purity %", "Benzene Purity %", "CAST(99.2 AS DECIMAL(5,2))"),
    (
        "Steam-to-Ethylene Ratio",
        "Steam-to-Ethylene Ratio",
        "CAST(1.8 AS FLOAT) / NULLIF(CAST(1.0 AS FLOAT),0)",
    ),
    (
        "Reactor Conversion %",
        "Reactor Conversion %",
        "100.0 * (950.0 / NULLIF(1000.0,0))",
    ),
    ("Flare Reduction %", "Flare Reduction %", "(1 - (15.0 / NULLIF(100.0,0))) * 100"),
    (
        "Compressor Availability %",
        "Compressor Availability %",
        "(720.0 / NULLIF(720.0+24.0,0)) * 100",
    ),
    (
        "Distillation Column Efficiency %",
        "Distillation Column Efficiency %",
        "(45.0 / NULLIF(50.0,0)) * 100",
    ),
]
for i, (n, a, e) in enumerate(tsql_items, start=1):
    w(OUT / f"tsql_kpi_{i:02d}.tsql", tsql_file(n, a, e))

# PL/SQL 6 (3 specs + 3 bodies)
plsql_defs = [
    ("Reactor Selectivity %", "reactor_selectivity", "(a / NULLIF(b,0)) * 100"),
    ("Furnace OEE %", "furnace_oee", "(0.92 * 0.95 * 0.98) * 100"),
    ("Hydrogen Compressor Efficiency %", "compressor_eff", "(a / NULLIF(b,0)) * 100"),
]
for i, (n, func, expr) in enumerate(plsql_defs, start=1):
    w(OUT / f"plsql_kpi_{i:02d}.pks", plsql_spec(n, func))
    w(OUT / f"plsql_kpi_{i:02d}.pkb", plsql_body(n, func, expr))

# HANA 6 (3 .hdbview, 3 .sqlscript)
hana_defs = [
    (
        "Cracker Throughput (t/day)",
        "Cracker Throughput (t/day)",
        "(100.0 / 24.0) * 24.0",
    ),
    ("Steam Ratio", "Steam Ratio", "(1.8 / 1.0)"),
    ("Ethane Conversion %", "Ethane Conversion %", "(950.0 / 1000.0) * 100"),
]
for i, (n, a, e) in enumerate(hana_defs, start=1):
    w(OUT / f"hana_kpi_{i:02d}.hdbview", hana_view(n, a, e))
    w(OUT / f"hana_kpi_{i:02d}.sqlscript", hana_view(n, a, e))

# Python 6
py_defs = [
    ("Furnace OEE %", "(0.92 * 0.95 * 0.98) * 100"),
    ("Ethylene Yield %", "(good / total) * 100"),
    ("Compressor MTBF (hours)", "(8760.0 / max(1.0, 12.0))"),
    ("Plant Availability %", "(uptime / (uptime + downtime)) * 100"),
    ("Energy Intensity (GJ/ton)", "(energy_gj / max(0.001, tons))"),
    ("Water Reuse %", "(reused / max(0.001, intake)) * 100"),
]
for i, (n, e) in enumerate(py_defs, start=1):
    # diversify variable names in body
    if "uptime" in e:
        body = """# KPI: Plant Availability %\n\ndef calc():\n    uptime = 720.0\n    downtime = 24.0\n    result = (uptime / (uptime + downtime)) * 100\n    return result\n"""
    elif "energy_gj" in e:
        body = """# KPI: Energy Intensity (GJ/ton)\n\ndef calc():\n    energy_gj = 52000.0\n    tons = 8500.0\n    result = (energy_gj / max(0.001, tons))\n    return result\n"""
    elif "reused" in e:
        body = """# KPI: Water Reuse %\n\ndef calc():\n    reused = 8200.0\n    intake = 10000.0\n    result = (reused / max(0.001, intake)) * 100\n    return result\n"""
    elif "MTBF" in n:
        body = """# KPI: Compressor MTBF (hours)\n\ndef calc():\n    failures = 12.0\n    total_hours = 8760.0\n    result = (total_hours / max(1.0, failures))\n    return result\n"""
    elif "Ethylene Yield" in n:
        body = """# KPI: Ethylene Yield %\n\ndef calc():\n    good = 8200.0\n    total = 10000.0\n    result = (good / total) * 100\n    return result\n"""
    else:
        body = python_file(n, e)
    w(OUT / f"python_kpi_{i:02d}.py", body)

# DAX 4
dax_defs = [
    ("Polymer Conversion %", "DIVIDE([ConvertedMass],[FeedMass]) * 100"),
    ("On-Stream Factor %", "DIVIDE([OnStreamHours],[TotalHours]) * 100"),
    ("Quality Rate %", "DIVIDE([GoodUnits],[TotalUnits]) * 100"),
    ("Flaring Ratio", "DIVIDE([FlareVolume],[ProducedGas])"),
]
for i, (n, e) in enumerate(dax_defs, start=1):
    w(OUT / f"dax_kpi_{i:02d}.dax", dax_file(n, e))

# C# 4
cs_defs = [
    ("Compressor MTBF (hours)", "totalHours / Math.Max(1, failures)"),
    ("Yield %", "(a / b) * 100.0"),
    ("Availability %", "(a / (a + b)) * 100.0"),
    ("Energy Intensity", "a / Math.Max(1.0, b)"),
]
for i, (n, e) in enumerate(cs_defs, start=1):
    content = cs_file(n, e).replace("totalHours", "8760").replace("failures", "12")
    w(OUT / f"cs_kpi_{i:02d}.cs", content)

# VB 4
vb_defs = [
    ("Compressor MTTR (minutes)", "downtime / Math.Max(1.0, failures)"),
    ("Yield %", "(a / b) * 100.0"),
    ("Availability %", "(a / (a + b)) * 100.0"),
    ("Steam Ratio", "a / Math.Max(1.0, b)"),
]
for i, (n, e) in enumerate(vb_defs, start=1):
    content = vb_file(n, e).replace("downtime", "1440").replace("failures", "6")
    w(OUT / f"vb_kpi_{i:02d}.vb", content)

# ABAP 3
abap_defs = [
    ("Steam-to-Ethylene Ratio", "a / b"),
    ("Yield %", "( a / b ) * 100"),
    ("Availability %", "( a / ( a + b ) ) * 100"),
]
for i, (n, e) in enumerate(abap_defs, start=1):
    w(OUT / f"abap_kpi_{i:02d}.abap", abap_file(n, e))

# IEC ST 3
st_defs = [
    ("Reactor Availability %", "(UpTime / (UpTime + DownTime)) * 100"),
    ("Yield %", "(a / b) * 100.0"),
    ("Flaring Ratio", "a / b"),
]
for i, (n, e) in enumerate(st_defs, start=1):
    w(OUT / f"st_kpi_{i:02d}.st", st_file(n, e))

print(f"Sample project generated at: {OUT}\nTotal files: {len(list(OUT.iterdir()))}")
