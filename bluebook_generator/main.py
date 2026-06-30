import os
import hashlib
import json
import jinja2
import re
import shutil
import time
import subprocess
from pathlib import Path
from urllib.parse import quote, urlencode
from .kpi_extractor import find_kpis_in_directory
from .ai_generator import generate_kpi_details
from .governance import attach_governance

# Public API from this module
__all__ = ["generate_bluebook"]

ROOT_DIR = Path(__file__).parent.parent
DOCS_SOURCE_DIR = ROOT_DIR / "docs"
TEMPLATE_DIR = ROOT_DIR / "templates"
UNMAPPED_DEVELOPER_LINEAGE = (
    "UNMAPPED: Utility logic detected without explicit database schema lineage."
)
DEFINITION_OVERRIDE_FIELDS = {
    "description",
    "objective",
    "formula_description",
    "used_in_kpis",
    "input_measure",
    "unit_of_measure",
    "reporting_source",
    "comments",
}


def _load_json_file(path: Path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return default
    return default


def _definition_override_candidates(kpi: dict) -> list[str]:
    candidates = [
        str(kpi.get("name") or "").strip(),
        str(kpi.get("function_name") or "").strip(),
        str(kpi.get("source_file_display") or "").strip(),
        Path(str(kpi.get("file_path") or "")).stem,
    ]
    return [c for c in candidates if c]


def _load_definition_overrides() -> dict:
    merged: dict = {}
    docs_overrides = _load_json_file(DOCS_SOURCE_DIR / "overrides.json", {})
    if isinstance(docs_overrides, dict):
        for name, fields in docs_overrides.items():
            if isinstance(fields, dict):
                merged[name] = {
                    "status": "APPROVED_BY_BUSINESS",
                    "fields": fields,
                    "source": "docs/overrides.json",
                }
    for override_path in (
        ROOT_DIR / "kb" / "overrides.json",
        ROOT_DIR / "bluebook_generator" / "kb" / "overrides.json",
    ):
        kb_overrides = _load_json_file(override_path, {})
        kb_kpis = kb_overrides.get("kpis", {}) if isinstance(kb_overrides, dict) else {}
        if isinstance(kb_kpis, dict):
            for name, block in kb_kpis.items():
                if isinstance(block, dict):
                    fields = block.get("fields", {})
                    if isinstance(fields, dict):
                        merged[name] = {
                            "status": block.get("status") or "APPROVED_BY_BUSINESS",
                            "fields": fields,
                            "source": str(override_path.relative_to(ROOT_DIR)),
                            "file_signature": block.get("file_signature") or "",
                        }
    return merged


def _apply_definition_override(kpi: dict, details: dict, overrides: dict) -> dict:
    if not overrides:
        return details
    override = None
    for candidate in _definition_override_candidates(kpi):
        if candidate in overrides:
            override = overrides[candidate]
            break
    if not override:
        return details
    override_signature = str(override.get("file_signature") or "").strip()
    current_signature = str(kpi.get("source_file_signature") or "").strip()
    if override_signature and override_signature != current_signature:
        return details
    fields = override.get("fields", {}) if isinstance(override, dict) else {}
    if not isinstance(fields, dict):
        return details
    updated = dict(details or {})
    for key in DEFINITION_OVERRIDE_FIELDS:
        value = fields.get(key)
        if value is not None and str(value).strip():
            updated[key] = value
    updated["_override_status"] = override.get("status") or "APPROVED_BY_BUSINESS"
    updated["_override_source"] = override.get("source") or "manual override ledger"
    return updated


def _sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        text = "" if text is None else str(text)
    s = text
    s = re.sub(r"(?is)<\s*(script|style)\b.*?>.*?<\s*/\s*\1\s*>", "", s)
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def format_text_as_html_list(text: str) -> str:
    from html import escape

    cleaned = _sanitize_text(text)
    safe = escape(cleaned)
    if not safe or "Error generating content" in safe:
        return f"<p>{safe}</p>"
    bullet_items = re.findall(r"(?:^|\n)\s*(?:[-*•]|\d+[.)])\s+(.+)", cleaned)
    if bullet_items:
        items = [escape(i.strip()) for i in bullet_items if len(i.strip()) > 1]
        return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
    return f"<p>{safe}</p>"


def _extract_function_block(code_context: str, anchor_line_number: int):
    import ast

    lines = code_context.splitlines()
    if not lines or anchor_line_number <= 0 or anchor_line_number > len(lines):
        return code_context, 0
    try:
        tree = ast.parse(code_context)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                start = node.lineno
                end = getattr(node, "end_lineno", None)
                if end is None:
                    last = node.body[-1]
                    end = getattr(last, "end_lineno", getattr(last, "lineno", start))
                if start <= anchor_line_number <= end:
                    return "\n".join(lines[start - 1 : end]), start - 1
    except Exception:
        pass
    anchor_idx = anchor_line_number - 1
    start_idx = 0
    for i in range(anchor_idx, -1, -1):
        if lines[i].lstrip().startswith("def "):
            start_idx = i
            break
    def_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())
    end_idx = len(lines)
    for j in range(start_idx + 1, len(lines)):
        raw = lines[j]
        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip())
        if not stripped:
            continue
        if raw.lstrip().startswith("def ") and indent <= def_indent:
            end_idx = j
            break
        if indent < def_indent:
            end_idx = j
            break
        if indent == 0 and (
            stripped.startswith("#") or stripped.startswith("if __name__")
        ):
            end_idx = j
            break
    scoped = "\n".join(lines[start_idx:end_idx])
    return scoped, start_idx


def generate_formula_from_code(code_context: str) -> dict:
    """
    Programmatically generate a MathJax block from code context.
    Supports:
    - DAX: DEFINE MEASURE 'T'[Name] = ... RETURN <expr> | Name = <expr>
    - SQL/T-SQL/HANA: SELECT <expr> AS <alias> (multi-line, CAST/CASE supported)
    - C#/VB/PLSQL/ABAP: return <expr>; or <var> = <expr>;
    - IEC 61131-3 ST: <var> := <expr>;
    - Generic fallback: pick the most math-like expression (percent or division) anywhere in the block.
    """
    formula_data = {
        "formula_html": "<p>See code context for implementation details.</p>",
        "formula_expression": "",
        "formula_result_name": "",
    }

    ctx = code_context

    # 0) Helpers

    def latex_escape(s: str) -> str:
        repl = [
            ("\\", r"\\"),
            ("{", r"\{"),
            ("}", r"\}"),
            ("_", r"\_"),
            ("^", r"\^"),
            ("~", r"\~"),
        ]
        out = s
        for a, b in repl:
            out = out.replace(a, b)
        return out

    def sanitize_token(t: str) -> str:
        t = t.strip()
        t = re.sub(r"^[{}\[\];,\s]+|[{}\[\];,\s]+$", "", t)
        t = re.sub(r"^\s*#\s*", "Number of ", t)
        t = re.sub(r"^\s*%\s*", "Percent ", t)
        t = re.sub(r"^\s*\$\s*", "Dollar ", t)
        t = t.replace("#", " Number ")
        t = t.replace("$", " Dollar ")
        t = re.sub(r"%\s*([A-Za-z])", r"Percent \1", t)
        t = re.sub(r"\s+%", "", t)
        t = t.replace("%", " Percent ")
        t = t.replace("&", " and ")
        t = re.sub(r"[:\.]+", " ", t)
        t = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", t)
        t = t.replace("_", " ")
        t = re.sub(r"(?i)(maintenance)to(operating)", r"\1 to \2", t)
        t = re.sub(r"(?i)(cost)ratio", r"\1 ratio", t)
        t = re.sub(r"(?i)(feedstock)throughput", r"\1 throughput", t)
        t = re.sub(r"(?i)(error)rate", r"\1 rate", t)
        t = re.sub(r"(?i)(extraction)rate", r"\1 rate", t)
        t = re.sub(r"\s+", " ", t).strip()
        t = latex_escape(t)
        return t.title()

    def L(v: str) -> str:
        return r"\text{{{}}}".format(v)

    def strip_inline_comments(line: str) -> str:
        cleaned = line
        cleaned = re.split(r"--", cleaned, maxsplit=1)[0]
        cleaned = re.split(r"//", cleaned, maxsplit=1)[0]
        cleaned = re.split(r"\(\*", cleaned, maxsplit=1)[0]
        cleaned = re.split(r"(?<!:)\s'", cleaned, maxsplit=1)[0]
        cleaned = re.split(r"#", cleaned, maxsplit=1)[0]
        return cleaned.rstrip(" ;\t")

    def unwrap_sql_expr(expr: str) -> str:
        e = expr.strip()
        m = re.search(r"(?is)\bCAST\s*\(\s*(?P<inner>.+?)\s+AS\s+[^\)]+\)", e)
        if m:
            e = m.group("inner").strip()
        m = re.search(r"(?is)\bCOALESCE\s*\(\s*(?P<inner>.+?)\s*,\s*.+?\)", e)
        if m:
            e = m.group("inner").strip()
        e = re.sub(r"(?is)\bNULLIF\s*\(\s*(.+?)\s*,\s*.+?\)", r"\1", e)
        e = re.sub(r"[;{}]+$", "", e).strip()
        return strip_wrapping_parentheses(e)

    def strip_wrapping_parentheses(expr: str) -> str:
        e = expr.strip()
        while e.startswith("(") and e.endswith(")"):
            depth = 0
            wraps_entire_expr = True
            for idx, ch in enumerate(e):
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0 and idx != len(e) - 1:
                        wraps_entire_expr = False
                        break
            if not wraps_entire_expr:
                break
            e = e[1:-1].strip()
        return e

    def balance_parentheses(expr: str) -> str:
        e = expr.strip()
        while e.count(")") > e.count("(") and ")" in e:
            e = e[: e.rfind(")")] + e[e.rfind(")") + 1 :]
        while e.count("(") > e.count(")") and "(" in e:
            e = e[: e.find("(")] + e[e.find("(") + 1 :]
        return e.strip()

    def normalize_expression(expr: str) -> str:
        e = expr.strip()
        e = e.replace("×", "*").replace("÷", "/")
        e = re.sub(r"(?i)\bdivided\s+by\b", "/", e)
        e = re.sub(r"(?i)\bmultiplied\s+by\b", "*", e)
        e = re.sub(r"(?i)\bminus\b", "-", e)
        e = re.sub(r"(?i)\bplus\b", "+", e)
        e = re.sub(r"(?i)\s+based\s+on\b.*$", "", e)
        e = balance_parentheses(e)
        return e

    def split_top_level_operator(expr: str, operators: set[str]) -> tuple[str, str, str] | None:
        depth = 0
        for idx in range(len(expr) - 1, -1, -1):
            ch = expr[idx]
            if ch == "(":
                depth = max(depth - 1, 0)
            elif ch == ")":
                depth += 1
            elif ch in operators and depth == 0:
                if ch in {"+", "-"} and idx == 0:
                    continue
                lhs = expr[:idx].strip()
                rhs = expr[idx + 1 :].strip()
                if lhs and rhs:
                    return lhs, ch, rhs
        return None

    def split_top_level_division(expr: str) -> tuple[str, str] | None:
        split = split_top_level_operator(expr, {"/"})
        if split:
            return split[0], split[2]
        return None

    def split_top_level_product(expr: str) -> list[str]:
        parts = []
        depth = 0
        start = 0
        for idx, ch in enumerate(expr):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(depth - 1, 0)
            elif ch == "*" and depth == 0:
                part = expr[start:idx].strip()
                if part:
                    parts.append(part)
                start = idx + 1
        tail = expr[start:].strip()
        if tail:
            parts.append(tail)
        return parts

    def clean_operand(value: str) -> str:
        v = strip_wrapping_parentheses(normalize_expression(value))
        v = unwrap_sql_expr(v)
        v = re.sub(r"(?is)\bNULLIF\s*\(\s*(?P<inner>.+?)\s*,\s*0(?:\.0)?\s*\)", r"\g<inner>", v)
        v = re.sub(r"(?is)\bCOALESCE\s*\(\s*(?P<inner>.+?)\s*,\s*.+?\)", r"\g<inner>", v)
        v = re.sub(
            r"(?is)\b(?:SUM|AVG|MIN|MAX)\s*\(\s*(?P<inner>.+?)\s*\)",
            r"\g<inner>",
            v,
        )
        v = re.sub(r"(?is)\bCOUNT\s*\(\s*\*\s*\)", "Count", v)
        v = re.sub(r"(?is)\bCAST\s*\(\s*(?P<inner>.+?)\s+AS\s+.+?\)", r"\g<inner>", v)
        v = re.sub(r"(?is)\bDATEDIFF\s*\(.+?\)", "Date Difference", v)
        v = strip_wrapping_parentheses(v)
        return v.strip()

    def is_math_like(expr: str) -> bool:
        return bool(expr) and (
            any(op in expr for op in ("+", "-", "*", "/", "%", "×", "÷"))
            or bool(
                re.search(
                    r"(?i)\b(?:minus|plus|divided\s+by|multiplied\s+by)\b",
                    expr,
                )
            )
        )

    def is_weak_expr(expr: str) -> bool:
        e = clean_operand(expr).strip()
        if not e:
            return True
        if re.fullmatch(r"\d+(?:\.\d+)?", e):
            return True
        if re.search(r"(?i)\bplaceholder\b", e):
            return True
        if e.lower() in {"number", "return number"}:
            return True
        if e.lower() in {"nullif", "cast"}:
            return True
        return False

    def is_numeric_literal(value: str) -> bool:
        return bool(re.fullmatch(r"\d+(?:\.\d+)?", value.strip()))

    def render_latex_expr(expr: str) -> str:
        e = clean_operand(expr)
        if not e:
            return L("Value")

        sum_match = re.match(r"(?is)^sum\s+of\s+(?:all\s+)?(?P<item>.+)$", e)
        if sum_match:
            return r"\sum \text{{{}}}".format(sanitize_token(sum_match.group("item")))

        count_match = re.match(r"(?is)^count\s+of\s+(?P<item>.+)$", e)
        if count_match:
            return r"\operatorname{{count}}\left(\text{{{}}}\right)".format(
                sanitize_token(count_match.group("item"))
            )

        avg_match = re.match(r"(?is)^average\s+of\s+(?P<item>.+)$", e)
        if avg_match:
            return r"\operatorname{{avg}}\left({}\right)".format(
                render_latex_expr(avg_match.group("item"))
            )

        split = split_top_level_operator(e, {"+", "-"})
        if split:
            lhs, op, rhs = split
            return f"{render_latex_expr(lhs)} {op} {render_latex_expr(rhs)}"

        split = split_top_level_operator(e, {"/"})
        if split:
            lhs, _, rhs = split
            return r"\frac{{{}}}{{{}}}".format(
                render_latex_expr(lhs), render_latex_expr(rhs)
            )

        product_parts = split_top_level_product(e)
        if len(product_parts) > 1:
            return r" \times ".join(render_latex_expr(p) for p in product_parts)

        if is_numeric_literal(e):
            return e

        return L(sanitize_token(e))

    def note_label(expr: str) -> str:
        label = clean_operand(expr)
        label = re.sub(r"[:]+", " ", label)
        label = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", label)
        label = label.replace("_", " ")
        label = re.sub(r"\s+", " ", label).strip()
        return label.title()

    def compact_result_label(name: str) -> str:
        label = note_label(name)
        label = re.sub(r"^\s*[#%$]+\s*", "", label).strip()
        label = re.sub(r"(?i)^(?:Number|No\.?)\s+Of\s+", "", label).strip()
        label = re.sub(r"(?i)^Number\s+", "", label).strip()
        label = re.sub(r"(?i)^Percent\s+", "", label).strip()
        label = re.sub(r"(?i)^Dollar\s+", "", label).strip()
        label = re.sub(r"\s+", " ", label).strip()
        words = label.split()
        if len(words) > 4:
            label = " ".join(words[-4:])
        return label or "KPI"

    def aggregate_match(expr: str) -> tuple[str, str] | None:
        e = clean_operand(expr)
        m = re.match(r"(?is)^sum\s+of\s+(?:all\s+)?(?P<item>.+)$", e)
        if m:
            return "sum", note_label(m.group("item"))
        m = re.match(r"(?is)^count\s+of\s+(?:all\s+)?(?P<item>.+)$", e)
        if m:
            return "count", note_label(m.group("item"))
        m = re.match(r"(?is)^average\s+of\s+(?P<item>.+)$", e)
        if m:
            return "avg", note_label(m.group("item"))
        return None

    def find_top_level_as_positions(text: str) -> list[int]:
        positions = []
        depth = 0
        for m in re.finditer(r"(?is)\(|\)|\bAS\b", text):
            token = m.group(0).upper()
            if token == "(":
                depth += 1
            elif token == ")":
                depth = max(depth - 1, 0)
            elif depth == 0:
                positions.append(m.start())
        return positions

    def extract_select_clauses(text: str) -> list[str]:
        clauses = []
        select_re = re.compile(r"(?is)\bSELECT\b")
        from_re = re.compile(r"(?is)\bFROM\b")
        for match in select_re.finditer(text):
            start = match.end()
            depth = 0
            end = None
            idx = start
            while idx < len(text):
                ch = text[idx]
                if ch == "(":
                    depth += 1
                    idx += 1
                    continue
                if ch == ")":
                    depth = max(depth - 1, 0)
                    idx += 1
                    continue
                if depth == 0:
                    fm = from_re.match(text, idx)
                    if fm:
                        end = idx
                        break
                    if text[idx] == ";":
                        end = idx
                        break
                idx += 1
            if end is None:
                end = len(text)
            clause = text[start:end].strip()
            if clause:
                clauses.append(clause)
        return clauses

    def gd(m: re.Match | None, key: str, default: str = "") -> str:
        if not m:
            return default
        try:
            return m.groupdict().get(key, default)
        except Exception:
            return default

    # Prepare cleaned single lines for non-multiline patterns
    cleaned_lines = []
    for raw in ctx.splitlines():
        s = raw.strip()
        if not s or s.startswith(("#", "--", "//", "/*", "*", "'")):
            continue
        cleaned_lines.append(strip_inline_comments(raw).strip())

    # Improved extraction: handle SQL aliases properly
    def extract_result_name_and_expression(text: str) -> tuple[str | None, str | None]:
        """
        Scan the entire text for a plausible result name and a math expression.
        Returns (result_name, expression) or (None, None).
        """
        result_name = "Result"
        math_expr = None

        # Look for AS alias first (SQL/HANA). Prefer top-level SELECT clauses that
        # actually calculate something, not nested helper SELECTs.
        select_clauses = extract_select_clauses(text)
        scored_clauses = sorted(
            select_clauses,
            key=lambda c: (
                1 if find_top_level_as_positions(c) else 0,
                1 if is_math_like(c) else 0,
                -len(c),
            ),
            reverse=True,
        )
        for select_clause in scored_clauses:
            # Find the last top-level AS (not inside parentheses)
            # We'll find all AS occurrences and pick the last one not inside parentheses
            as_positions = find_top_level_as_positions(select_clause)
            if as_positions:
                last_as = as_positions[-1]
                alias = select_clause[last_as + 2 :].strip()
                # Clean alias (remove brackets, quotes, etc.)
                alias = re.sub(r'^[\[\("\']|[\]\)"\']$', "", alias)
                if alias:
                    result_name = alias
                expr = select_clause[:last_as].strip()
            else:
                expr = select_clause
            # Remove outer parentheses
            expr = strip_wrapping_parentheses(expr)
            # Unwrap SQL functions
            expr = unwrap_sql_expr(expr)
            if expr and (not is_weak_expr(expr) or re.search(r"(?is)\bCOUNT\s*\(\s*\*\s*\)", expr)):
                return result_name, expr
            if expr and result_name != "Result":
                return result_name, expr

        # Look for DAX measure definition
        dax_match = re.search(
            r"(?is)\bDEFINE\s+MEASURE\s+[^\[]*\[(?P<name>[^\]]+)\]\s*=\s*(?P<body>.+?)(?:$|\n\s*\n)",
            text,
        )
        if dax_match:
            name = gd(dax_match, "name")
            body = gd(dax_match, "body")
            if name and body:
                ret = re.search(r"(?is)\bRETURN\b\s*(?P<expr>.+)", body)
                if ret:
                    expr = gd(ret, "expr")
                    if expr:
                        return name, expr

        # Human formula text such as "Propylene to Ethylene (P/E) Ratio = A / B".
        human_assign = re.search(
            r"(?im)^\s*(?P<lhs>[^=\r\n]{1,120}?)\s*=\s*(?P<expr>.+?)(?:$|;|\n)",
            text,
        )
        if human_assign:
            lhs = human_assign.group("lhs").strip()
            expr = human_assign.group("expr").strip()
            if expr and (
                is_math_like(expr)
                or re.match(r"(?is)^\s*(?:sum|count)\s+of\b", expr)
            ):
                return lhs, expr

        # Look for simple assignments like "x = a / b" (Python, C#, etc.)
        assign_matches = list(
            re.finditer(
                r"(?im)^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?P<expr>.+?)(?:$|;|\n)",
                text,
            )
        )
        assign_matches.sort(
            key=lambda m: (is_math_like(m.group("expr")), not is_weak_expr(m.group("expr"))),
            reverse=True,
        )
        for assign_pattern in assign_matches:
            lhs = assign_pattern.group(1)
            expr = strip_inline_comments(assign_pattern.group("expr").strip())
            if expr and (is_math_like(expr) or not is_weak_expr(expr)):
                if result_name == "Result":
                    result_name = lhs
                return result_name, expr

        # Look for IEC ST assignment :=
        st_match = re.search(
            r"(?im)^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:=\s*(?P<expr>.+?)(?:$|;|\n)", text
        )
        if st_match:
            lhs = st_match.group(1)
            expr = st_match.group("expr").strip()
            if expr:
                if result_name == "Result":
                    result_name = lhs
                return result_name, expr

        # Look for return statements
        return_matches = list(re.finditer(r"(?im)\breturn\b\s+(?P<expr>[^;\r\n]+)", text))
        return_matches.sort(
            key=lambda m: (is_math_like(m.group("expr")), not is_weak_expr(m.group("expr"))),
            reverse=True,
        )
        for ret_match in return_matches:
            expr = ret_match.group("expr").strip()
            if expr and (is_math_like(expr) or not is_weak_expr(expr)):
                return result_name, expr

        # If nothing, look for any line with a fraction or percent pattern
        pct_lines = re.findall(
            r"(?is)(\d*\.?\d+\s*\*\s*100|100\s*\*\s*\d*\.?\d+)", text
        )
        if pct_lines:
            expr = pct_lines[0]
            return result_name, expr

        # Look for any division or multiplication
        div_match = re.search(
            r"(?is)([a-zA-Z0-9_\.\s]+)\s*/\s*([a-zA-Z0-9_\.\s]+)", text
        )
        if div_match:
            a, b = div_match.groups()
            expr = f"{a.strip()} / {b.strip()}"
            return result_name, expr

        return None, None

    def build_html(result_var: str, expression: str) -> dict:
        rv = sanitize_token(compact_result_label(result_var))
        expr = strip_wrapping_parentheses(normalize_expression(expression.strip().rstrip(";")))
        notes = []
        aggregate = aggregate_match(expr)
        if aggregate:
            aggregate_type, aggregate_item = aggregate
            if aggregate_type == "sum":
                latex_str = r"{} = \sum_{{i=1}}^{{N}} 1".format(L(rv))
            elif aggregate_type == "count":
                latex_str = r"{} = \operatorname{{count}}(T)".format(L(rv))
            else:
                latex_str = r"{} = {}".format(L(rv), render_latex_expr(expr))
            if aggregate_type == "avg":
                notes = [
                    f"<i>Expression:</i> {aggregate_item}",
                    "<i>Rule:</i> Average the calculated value across qualifying records in the reporting period.",
                ]
            else:
                notes = [
                    f"<i>N / T:</i> {aggregate_item}",
                    "<i>Rule:</i> Count each qualifying record once in the reporting period.",
                ]
        else:
            latex_str = r"{} = {}".format(L(rv), render_latex_expr(expr))

        divisor = split_top_level_division(strip_wrapping_parentheses(expr))
        if divisor and not aggregate:
            notes = [
                f"<i>Numerator:</i> {note_label(divisor[0])}",
                f"<i>Denominator:</i> {note_label(divisor[1])}",
            ]

        if latex_str:
            notes_html = (
                "<p><b>Where:</b></p><ul>"
                + "".join(f"<li>{n}</li>" for n in notes)
                + "</ul>"
                if notes
                else ""
            )
            return {
                "formula_html": f'<div class="math-equation">\\[ {latex_str} \\]</div>{notes_html}',
                "formula_expression": expr,
                "formula_result_name": result_var,
            }

        return {"formula_html": "<p>See code context for implementation details.</p>"}

    # --- Main extraction ---
    result_name, math_expr = extract_result_name_and_expression(ctx)
    if result_name and math_expr:
        return build_html(result_name, math_expr)

    # Fallback: try to find any math-like expression in cleaned lines
    for line in cleaned_lines:
        if "/" in line or "*" in line:
            match = re.search(r"([a-zA-Z0-9_\.\s]+)\s*/\s*([a-zA-Z0-9_\.\s]+)", line)
            if match:
                a, b = match.groups()
                expr = f"{a.strip()} / {b.strip()}"
                name_match = re.search(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=", line)
                res_name = "Result"
                if name_match:
                    res_name = sanitize_token(name_match.group(1))
                return build_html(res_name, expr)

    return formula_data


def create_rst_file(
    kpi_data: dict,
    details: dict,
    template: jinja2.Template,
    ai_time_seconds: float | None = None,
):
    from html import escape
    import time

    render_start = time.perf_counter()
    kpi_line_in_context = 0
    context_lines = (kpi_data.get("code_context") or "").split("\n")
    kpi_name = kpi_data.get("name") or ""
    for i, line in enumerate(context_lines):
        if (
            f"# KPI: {kpi_name}" in line
            or f"-- KPI: {kpi_name}" in line
            or f"' KPI: {kpi_name}" in line
            or f"/* KPI: {kpi_name}" in line
        ):
            kpi_line_in_context = i + 1
            break
    kpi_data["context_line_number"] = kpi_line_in_context
    file_path = kpi_data.get("file_path") or ""
    try:
        source_line_number = int(
            kpi_data.get("file_line") or kpi_data.get("context_line_number") or 1
        )
    except (TypeError, ValueError):
        source_line_number = 1
    if source_line_number < 1:
        source_line_number = 1
    kpi_data["source_line_number"] = source_line_number
    kpi_data["has_source_link"] = bool(str(file_path).strip())
    if kpi_data["has_source_link"]:
        source_path = Path(str(file_path)).expanduser()
        if not source_path.is_absolute():
            source_path = (ROOT_DIR / source_path).resolve()
        else:
            source_path = source_path.resolve()
        vscode_path = quote(str(source_path), safe="/:%")
        pycharm_path = quote(str(source_path), safe="/:")
        kpi_data["vscode_url"] = f"vscode://file{vscode_path}:{source_line_number}"
        kpi_data["pycharm_url"] = (
            f"pycharm://open?file={pycharm_path}&line={source_line_number}"
        )
    else:
        kpi_data["vscode_url"] = ""
        kpi_data["pycharm_url"] = ""
    if file_path:
        try:
            display_base = Path(kpi_data.get("source_root") or ROOT_DIR).expanduser().resolve()
            kpi_data["source_file_display"] = str(Path(file_path).expanduser().resolve().relative_to(display_base))
        except Exception:
            kpi_data["source_file_display"] = str(file_path)
    else:
        kpi_data["source_file_display"] = ""
    kpi_data["source_language_display"] = (kpi_data.get("language") or "unknown").upper()
    kpi_data["detection_kind_display"] = (
        str(kpi_data.get("detection_kind") or kpi_data.get("_kind") or "unspecified")
        .replace("_", " ")
        .title()
    )
    try:
        kpi_data["confidence_display"] = f"{float(kpi_data.get('confidence', 0)):.0f}%"
    except Exception:
        kpi_data["confidence_display"] = "0%"
    kpi_data["code_hash"] = hashlib.md5(
        (kpi_data.get("code_context") or "").encode("utf-8")
    ).hexdigest()[:10]
    identity_source = " ".join(
        str(kpi_data.get(key) or "")
        for key in ("name", "file_path", "code_context", "source_file_display")
    )
    identity_match = re.search(r"\bKPI[-_\s]?\d+\b", identity_source, re.I)
    if identity_match:
        kpi_data["kpi_identity_display"] = (
            identity_match.group(0).replace(" ", "").replace("_", "-").upper()
        )
    else:
        kpi_data["kpi_identity_display"] = f"KPI-{kpi_data['code_hash'].upper()}"
    governance = kpi_data.get("governance") or {}
    kpi_data["governance_responsible"] = governance.get("responsible") or ""
    kpi_data["governance_accountable"] = governance.get("accountable") or ""
    kpi_data["governance_consulted"] = governance.get("consulted") or ""
    kpi_data["governance_informed"] = governance.get("informed") or ""
    kpi_data["governance_basis"] = governance.get("basis") or ""
    kpi_data["governance_method"] = governance.get("method") or ""
    kpi_data["governance_confidence"] = governance.get("confidence") or ""
    domain = re.sub(
        r"\s*(Data Owner|Owner|Team|Department)\s*$",
        "",
        kpi_data["governance_accountable"],
        flags=re.I,
    ).strip()
    kpi_data["governance_domain_display"] = domain or "Enterprise KPI"
    _, ext = os.path.splitext(str(file_path).lower())
    if ext == ".py":
        scoped_context, start_idx = _extract_function_block(
            kpi_data.get("code_context", ""), kpi_line_in_context
        )
        kpi_data["code_context"] = scoped_context
        if kpi_line_in_context > 0:
            rel = kpi_line_in_context - start_idx
            kpi_data["context_line_number"] = rel if rel > 0 else 0
        else:
            kpi_data["context_line_number"] = 0
        programmatic_formula = generate_formula_from_code(scoped_context)
    else:
        programmatic_formula = generate_formula_from_code(
            kpi_data.get("code_context", "")
        )
    formula_description_raw = details.get("formula_description", "") or ""

    def _looks_like_formula(text: str) -> bool:
        if not isinstance(text, str):
            return False
        s = text.strip()
        if not s:
            return False
        if "derived directly from the code" in s.lower():
            return False
        return any(op in s for op in ("/", "*", "×", "÷", "+", "-")) or bool(
            re.search(
                r"(?i)\b(?:minus|plus|divided\s+by|multiplied\s+by|sum\s+of|count\s+of)\b",
                s,
            )
        )

    def _formula_html_quality(formula_html: str) -> int:
        s = formula_html or ""
        if not s or "See code context" in s:
            return 0
        score = 2
        weak_bits = (
            "Placeholder",
            "= 0.0",
            "Nullif",
            "\\text{Count}",
            "\\text{Cast}",
            "\\text{Date Difference}",
            "\\text{Number}",
            "\\text{Return}",
        )
        if any(bit in s for bit in weak_bits):
            score -= 1
        if "\\frac" in s or "\\times" in s:
            score += 1
        return score

    formula_mismatch = False
    formula_mismatch_reason = ""
    if _looks_like_formula(formula_description_raw):
        formula_from_description = generate_formula_from_code(
            f"{kpi_name or 'Result'} = {formula_description_raw}"
        )
        description_quality = _formula_html_quality(formula_from_description.get("formula_html", ""))
        programmatic_quality = _formula_html_quality((programmatic_formula or {}).get("formula_html", ""))
        description_ops = set(re.findall(r"[+\-*/×÷]", formula_description_raw))
        programmatic_html = (programmatic_formula or {}).get("formula_html", "")
        programmatic_ops = set()
        if "\\frac" in programmatic_html:
            programmatic_ops.add("/")
        if "\\times" in programmatic_html:
            programmatic_ops.add("*")
        if " - " in programmatic_html:
            programmatic_ops.add("-")
        if " + " in programmatic_html:
            programmatic_ops.add("+")
        source_operator_lines = []
        for raw_line in (kpi_data.get("code_context") or "").splitlines():
            source_line = raw_line.strip()
            if not source_line:
                continue
            if source_line.startswith(("--", "#", "//", "'")):
                if not re.search(r"(?i)\b(compute|computes|calculation|formula)\b", source_line):
                    continue
                source_line = re.sub(r"^(?:--|#|//|')\s*", "", source_line)
            source_operator_lines.append(source_line)
        source_ops = set(re.findall(r"[+\-*/×÷]", "\n".join(source_operator_lines)))
        source_ops_normalized = set()
        if {"÷", "/"} & source_ops:
            source_ops_normalized.add("/")
        if {"×", "*"} & source_ops:
            source_ops_normalized.add("*")
        if "-" in source_ops:
            source_ops_normalized.add("-")
        if "+" in source_ops:
            source_ops_normalized.add("+")
        evidence_ops = programmatic_ops | source_ops_normalized
        clear_business_formula = description_quality > 0 and bool(description_ops)
        formula_mismatch = clear_business_formula and not (
            bool({"-", "+"} & description_ops & evidence_ops)
            or (bool({"/", "÷"} & description_ops) and "/" in evidence_ops)
            or (bool({"*", "×"} & description_ops) and "*" in evidence_ops)
        )
        if formula_mismatch:
            # Provide an ISO-22400 aligned conflict signal and clear administrative phrasing.
            formula_mismatch_reason = (
                "The operational logic defined by business documentation does not align "
                "with the execution path verified in the source repository code."
            )
        # Expose a top-level governance conflict flag on the KPI record for template logic
        # and downstream tooling. This is intentionally a boolean that surfaces an
        # "ISO Compliance & Governance Conflict" state when true.
        try:
            # Some callers build kpi_data earlier; ensure the key exists for templates.
            kpi_data["governance_conflict"] = bool(formula_mismatch)
        except Exception:
            pass
        if description_quality >= programmatic_quality or formula_mismatch:
            programmatic_formula = formula_from_description
    # If a governance/formula mismatch was detected, label it explicitly as an
    # ISO compliance conflict in the human-readable reason so the UI can show a
    # clear administrative warning.
    if formula_mismatch:
        formula_mismatch_reason = "ISO Compliance & Governance Conflict: " + formula_mismatch_reason

    # Variable to store LaTeX formula HTML if detected
    latex_formula_html = None

    # Check for explicit LaTeX formula in kpi_data before processing programmatic formula
    explicit_formula = str(kpi_data.get("formula") or "").strip()
    if explicit_formula and any(char in explicit_formula for char in ["\\", r"\frac", r"\mathrm"]):
        # Wrap LaTeX in MathJax HTML format with \[ \] delimiters
        latex_formula_html = f'<div class="math-equation">\\[ {explicit_formula} \\]</div>'
        # Override programmatic_formula with the LaTeX formula
        programmatic_formula = {"formula_html": latex_formula_html}

    final_details = {
        "description_html": format_text_as_html_list(details.get("description", "")),
        "objective_html": format_text_as_html_list(details.get("objective", "")),
        "formula_description": escape(formula_description_raw),
        "used_in_kpis_html": format_text_as_html_list(details.get("used_in_kpis", "")),
        "input_measure_html": format_text_as_html_list(
            details.get("input_measure", "")
        ),
        "unit_of_measure": escape(details.get("unit_of_measure", "") or ""),
        "reporting_source": escape(details.get("reporting_source", "") or ""),
        "comments": escape(details.get("comments", "") or ""),
        **(programmatic_formula or {}),
    }

    def _plain_text(value: str) -> str:
        text = _sanitize_text(value or "")
        text = re.sub(r"^(?:[-*•]|\d+[.)])\s*", "", text).strip()
        return text

    def _is_undetermined_text(value: str) -> bool:
        normalized = str(value or "").upper()
        return "UNDETERMINED" in normalized or "LINEAGE UNDETERMINED" in normalized

    def _first_sentence(value: str, fallback: str) -> str:
        text = _plain_text(value)
        if not text:
            return fallback
        match = re.search(r"^(.{25,220}?[.!?])(?:\s|$)", text)
        if match:
            return match.group(1).strip()
        return text[:220].rstrip(" ,;") + ("." if not text.endswith(".") else "")

    def _business_formula_sentence() -> str:
        formula_text = _plain_text(formula_description_raw)
        if formula_text and not _is_undetermined_text(formula_text):
            return formula_text[0].upper() + formula_text[1:]
        
        source_formula = str((programmatic_formula or {}).get("formula_expression") or "").strip()
        if source_formula:
            return source_formula
        
        explicit_formula = str(kpi_data.get("formula") or "").strip()
        if explicit_formula:
            # Check for LaTeX syntax (backslashes, common LaTeX keywords)
            if any(char in explicit_formula for char in ["\\", r"\frac", r"\mathrm"]):
                try:
                    formula_res = generate_formula_from_code(f"Result = {explicit_formula}")
                    if formula_res and formula_res.get("formula_expression"):
                        return formula_res["formula_expression"]
                except Exception:
                    pass # Fallback to raw if processing fails
            return explicit_formula
        
        return (
            f"{kpi_name or 'This KPI'} is calculated from the extracted source logic "
            "shown in the evidence block."
        )

    def _movement_language(name: str) -> tuple[str, str]:
        lowered = (name or "").lower()
        negative_terms = (
            "complaint",
            "churn",
            "loss",
            "cost",
            "emission",
            "error",
            "failure",
            "downtime",
            "defect",
        )
        positive_terms = (
            "yield",
            "efficiency",
            "availability",
            "purity",
            "recovery",
            "utilization",
            "conversion",
            "selectivity",
            "oee",
            "service factor",
        )
        if any(term in lowered for term in negative_terms):
            return (
                "Usually signals a higher burden, risk, or exception volume that should be reviewed by the accountable owner.",
                "Usually signals lower burden or improved control, provided the data capture process has not changed.",
            )
        if any(term in lowered for term in positive_terms):
            return (
                "Usually signals better operating performance, assuming the denominator and period filters are unchanged.",
                "Usually signals weaker performance or a possible data-quality issue that should be investigated.",
            )
        return (
            "Indicates a material change in the measured business condition and should be interpreted with the owner.",
            "Indicates a material change in the measured business condition and should be checked against source-data timing.",
        )

    def _evidence_snippet() -> str:
        lines = (kpi_data.get("code_context") or "").splitlines()
        if not lines:
            return "No source code context was captured for this KPI."
        anchor = int(kpi_data.get("context_line_number") or 1)
        if anchor <= 0:
            anchor = 1
        start = max(0, anchor - 3)
        end = min(len(lines), anchor + 4)
        numbered = []
        for offset, line in enumerate(lines[start:end], start=start + 1):
            numbered.append(f"{offset:>4} | {line}")
        return "\n".join(numbered)

    def _developer_tokens_from_source() -> list[str]:
        source = "\n".join(
            raw
            for raw in (kpi_data.get("code_context") or "").splitlines()
            if raw.strip()
            and not raw.strip().startswith(("#", "--", "//", "/*", "*", "'"))
        )
        tokens: list[str] = []
        seen = set()
        patterns = (
            r"\b[A-Z][A-Z0-9_]{2,}\b",
            r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\(",
            r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
        )
        stop_words = {
            "KPI",
            "CREATE",
            "OR",
            "REPLACE",
            "PACKAGE",
            "FUNCTION",
            "RETURN",
            "NUMBER",
            "END",
            "SELECT",
            "FROM",
            "WHERE",
            "CAST",
            "NULLIF",
            "SUM",
            "COUNT",
            "CASE",
            "WHEN",
            "THEN",
            "ELSE",
        }
        for pattern in patterns:
            for match in re.finditer(pattern, source):
                token = match.group(0).strip().rstrip("(").strip()
                if len(token) < 3 or token.upper() in stop_words:
                    continue
                if token not in seen:
                    seen.add(token)
                    tokens.append(token)
                if len(tokens) >= 24:
                    return tokens
        return tokens

    def _token_key(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", value.lower())

    def _developer_label_for(business_label: str, developer_tokens: list[str]) -> str:
        business_key = _token_key(business_label)
        if not business_key:
            return UNMAPPED_DEVELOPER_LINEAGE

        def _format_mapping(token: str) -> str:
            lang = (kpi_data.get("language") or "").lower()
            if lang == "python":
                return f"VARIABLE: {token}"
            if lang in {"sql", "tsql", "plsql", "hana"}:
                return f"COLUMN: {token}"
            return f"SOURCE TOKEN: {token}"

        token_pairs = [
            (token, _token_key(token))
            for token in developer_tokens
            if _token_key(token)
        ]
        for token, token_key in token_pairs:
            if token_key == business_key:
                return _format_mapping(token)
        for token, token_key in sorted(token_pairs, key=lambda item: len(item[1]), reverse=True):
            if business_key in token_key:
                return _format_mapping(token)
        for token, token_key in sorted(token_pairs, key=lambda item: len(item[1]), reverse=True):
            if token_key in business_key:
                return _format_mapping(token)
        business_words = [w for w in re.findall(r"[a-z0-9]+", business_label.lower()) if len(w) > 2]
        for token, token_key in sorted(token_pairs, key=lambda item: len(item[1]), reverse=True):
            if business_words and any(word in token_key for word in business_words):
                return _format_mapping(token)
        return UNMAPPED_DEVELOPER_LINEAGE

    def _code_role_for_line(line: str) -> str:
        clean = line.strip().rstrip(";")
        if clean in {"/", "GO"}:
            return "Execution delimiter: separates or submits the database package statement."
        if re.search(r"(?i)\b(compute|computes|calculation|formula)\b", clean):
            return "Calculation hint: documents the business expression expected inside the KPI implementation."
        if clean.startswith(("--", "#", "//", "'")):
            return "KPI marker: tells LEAP this nearby code defines or documents a KPI."
        if re.search(r"(?i)\bCREATE\s+OR\s+REPLACE\s+PACKAGE\b", clean):
            return "Package boundary: declares the interface where this KPI routine is published."
        function_match = re.search(r"(?i)\bFUNCTION\s+([a-zA-Z_][a-zA-Z0-9_]*)", clean)
        if function_match:
            if re.search(r"(?i)\bRETURN\s+NUMBER\b", clean):
                return (
                    f"KPI function: {function_match.group(1)} exposes this metric; "
                    "RETURN NUMBER declares the KPI result as numeric output."
                )
            return f"KPI function: {function_match.group(1)} is the callable routine that exposes this metric."
        if re.search(r"(?i)\bRETURN\s+NUMBER\b", clean):
            return "Return contract: the KPI output is numeric and can be used in calculations, dashboards, or thresholds."
        if re.search(r"(?i)\bEND\b", clean):
            return "Scope boundary: closes the KPI package, function, or code block."
        if re.search(r"(?i)\bSELECT\b", clean):
            return "Query entry point: starts the data-selection logic used to calculate the KPI."
        if re.search(r"(?i)\bAS\s+[a-zA-Z_][a-zA-Z0-9_]*\b", clean):
            alias = re.search(r"(?i)\bAS\s+([a-zA-Z_][a-zA-Z0-9_]*)\b", clean)
            alias_text = alias.group(1) if alias else "the KPI output"
            return f"Output alias: maps this expression to {alias_text} in the result set."
        if re.search(r"[+\-*/×÷]", clean):
            return "Calculation expression: combines source variables used by the formal formula."
        if re.search(r"(?i)\bFROM\b", clean):
            return "Source relation: identifies the table, view, or dataset read by the KPI."
        return "Source context: supports the KPI definition or execution boundary."

    def _developer_lineage_html() -> str:
        lines = [line for line in (kpi_data.get("code_context") or "").splitlines() if line.strip()]
        if not lines:
            return ""
        rows = []
        for idx, line in enumerate(lines[:10], start=1):
            clean = line.strip()
            if len(clean) > 120:
                clean = clean[:117].rstrip() + "..."
            rows.append(
                '<div class="leap-code-lineage-row">'
                f'<div class="leap-code-lineage-code">{escape(str(idx))} | {escape(clean)}</div>'
                f'<div class="leap-code-lineage-role">{escape(_code_role_for_line(clean))}</div>'
                "</div>"
            )
        return (
            '<div class="leap-code-lineage" hidden>'
            '<div class="leap-code-lineage-title">Developer Lineage Breakdown</div>'
            + "".join(rows)
            + "</div>"
        )

    def _display_formula_symbol(token: str) -> str:
        mapping = {
            "*": "×",
            "×": "×",
            "/": "÷",
            "÷": "÷",
            "+": "+",
            "-": "-",
            "(": "(",
            ")": ")",
        }
        return mapping.get(token, token)

    def _business_label_for_code_token(token: str) -> str:
        cleaned = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", token.replace("_", " ")).strip()
        lower = cleaned.lower()
        compact = _token_key(cleaned)
        if compact in {"totalco2kg", "totalco2e", "totalco2emitted", "totalco2eemitted"}:
            return "Total Generated CO2e Emitted"
        if compact in {"grossgenerationmw", "netexportedgridmw", "netpowerexportedtogrid"}:
            return "Net Power Exported to Grid"
        if compact in {"totalinvoiceamt", "totalinvoiceamount"}:
            return "Total Invoice Amount"
        if compact in {"frameworkcontractamt", "frameworkcontractamount"}:
            return "Framework Contract Amount"
        if compact in {"totalcrackedliquids"}:
            return "Total Cracked Liquids"
        if compact in {"pureethyleneweight"}:
            return "Pure Ethylene Weight"
        if compact in {"feedstockinputweight"}:
            return "Feedstock Input Weight"
        if "accounts receivable" in lower:
            return "Accounts Receivable Balance"
        if "sales revenue" in lower or lower == "revenue":
            return "Total Sales Revenue"
        if "cash receipt" in lower:
            return "Cash Receipt Date"
        if "delivery date" in lower:
            return "Delivery Date"
        return cleaned.title() if cleaned else token

    def _math_symbol_for_token(token: str) -> str:
        cleaned = token.strip()
        compact = _token_key(cleaned)
        if compact == "accountsreceivable":
            return "AR"
        if compact == "salesrevenue":
            return "Revenue"
        if compact == "cashreceiptdate":
            return "Cash Receipt"
        if compact == "deliverydate":
            return "Delivery"
        if compact in {"totalco2kg", "totalco2e", "totalco2emitted", "totalco2eemitted"}:
            return "CO_2e"
        if compact in {"grossgenerationmw", "netexportedgridmw", "netpowerexportedtogrid"}:
            return "MWh"
        if compact in {"totalinvoiceamt", "totalinvoiceamount"}:
            return "Invoice"
        if compact in {"frameworkcontractamt", "frameworkcontractamount"}:
            return "Contract"
        if compact == "totalcrackedliquids":
            return "Liquids"
        if compact == "pureethyleneweight":
            return "Ethylene"
        if compact == "feedstockinputweight":
            return "Feedstock"
        if cleaned in {"*", "×"}:
            return "×"
        if cleaned in {"/", "÷"}:
            return "÷"
        return _display_formula_symbol(cleaned)

    def _operator_label(token: str) -> tuple[str, str, str]:
        if token in {"/", "÷"}:
            return "Divided By", "OPERATOR: /", "÷"
        if token in {"*", "×"}:
            return "Multiplied By", "OPERATOR: *", "×"
        if token == "-":
            return "Minus", "OPERATOR: -", "-"
        if token == "+":
            return "Plus", "OPERATOR: +", "+"
        if token == "(":
            return "Open Group", "GROUP: (", "("
        if token == ")":
            return "Close Group", "GROUP: )", ")"
        return _display_formula_symbol(token), f"OPERATOR: {token}", _display_formula_symbol(token)

    def _source_expression_for_annotation() -> str:
        formula_expr = str((programmatic_formula or {}).get("formula_expression") or "").strip()
        if formula_expr:
            return formula_expr
        source = kpi_data.get("code_context") or ""
        select_match = re.search(
            r"(?is)\bSELECT\b\s*(?P<expr>.+?)\s+\bAS\b\s+[a-zA-Z_][a-zA-Z0-9_]*",
            source,
        )
        if select_match:
            return select_match.group("expr").strip()
        return_match = re.search(r"(?im)\breturn\b\s+(?P<expr>[^;\r\n]+)", source)
        if return_match:
            return return_match.group("expr").strip()
        assign_match = re.search(
            r"(?im)\b[a-zA-Z_][a-zA-Z0-9_]*\s*[:=]\s*(?P<expr>[^;\r\n]+)",
            source,
        )
        if assign_match:
            return assign_match.group("expr").strip()
        return ""

    def _fallback_annotation_expression() -> str:
        candidates = [
            str((programmatic_formula or {}).get("formula_expression") or "").strip(),
            str(kpi_data.get("formula") or "").strip(),
            _source_expression_for_annotation(),
            _plain_text(formula_description_raw),
        ]
        for candidate in candidates:
            if candidate and not _is_undetermined_text(candidate):
                return candidate
        source = kpi_data.get("code_context") or ""
        math_lines: list[str] = []
        for raw in source.splitlines():
            line = raw.strip()
            if not line or line.startswith(("#", "--", "//", "/*", "*", "'")):
                continue
            if re.search(r"[+\-*/×÷]", line):
                math_lines.append(line)
        if math_lines:
            math_lines.sort(key=lambda line: ("return" in line.lower(), "/" in line or "*" in line, len(line)), reverse=True)
            line = math_lines[0]
            return_match = re.search(r"(?im)\breturn\b\s+(?P<expr>[^;\r\n]+)", line)
            if return_match:
                return return_match.group("expr").strip()
            assign_match = re.search(r"(?im)\b[a-zA-Z_][a-zA-Z0-9_]*\s*[:=]\s*(?P<expr>[^;\r\n]+)", line)
            if assign_match:
                return assign_match.group("expr").strip()
            return line
        function_match = re.search(r"(?im)\bdef\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", source)
        if function_match:
            return function_match.group(1)
        sql_alias = re.search(r"(?is)\bAS\s+([A-Za-z_][A-Za-z0-9_]*)\b", source)
        if sql_alias:
            return sql_alias.group(1)
        return kpi_name or kpi_data.get("name") or "Result"

    def _tokenize_formula_expression(expression: str) -> list[str]:
        expression = re.sub(
            r"(?is)\b(?:SUM|AVG|MIN|MAX)\s*\(\s*([^()]+?)\s*\)",
            r"\1",
            expression or "",
        )
        expression = re.sub(
            r"(?is)\bNULLIF\s*\(\s*([^,()]+?)\s*,\s*0(?:\.0)?\s*\)",
            r"\1",
            expression,
        )
        expression = re.sub(r"(?is)\breturn\b\s+", "", expression)
        expression = re.sub(r"(?is)\bAS\s+[A-Za-z_][A-Za-z0-9_]*\b.*$", "", expression)
        expression = re.sub(r"[;,]+$", "", expression.strip())
        return [
            re.sub(r"^[,\s]+|[,\s]+$", "", part.strip())
            for part in re.split(r"(\+|-|\*|/|×|÷|\(|\))", expression)
            if part and part.strip() and re.sub(r"^[,\s]+|[,\s]+$", "", part.strip())
        ]

    def _formula_node_html(
        business_label: str,
        developer_label: str,
        symbol: str,
        extra_class: str = "",
    ) -> str:
        token = _formula_node_token(business_label, developer_label, symbol, extra_class)
        return (
            f'<div class="leap-formula-node{escape(token["extra_class"], quote=True)}">'
            f'<span class="leap-math-lbl{" long-line" if token["long_label"] else ""}" '
            f'data-biz="{escape(token["business_label"], quote=True)}" '
            f'data-dev="{escape(token["developer_mapping"], quote=True)}">{escape(token["business_label"])}</span>'
            '<div class="leap-math-pointer"></div>'
            f'<span class="leap-math-render">{escape(token["math_symbol"])}</span>'
            "</div>"
        )

    def _formula_node_token(
        business_label: str,
        developer_label: str,
        symbol: str,
        extra_class: str = "",
    ) -> dict:
        business_label = _shorten_label(business_label, 56)
        developer_label = _shorten_label(developer_label, 56)
        symbol = _shorten_label(symbol, 24)
        return {
            "business_label": business_label,
            "developer_mapping": developer_label,
            "math_symbol": symbol,
            # Compatibility aliases for any downstream code that has not migrated.
            "developer_label": developer_label,
            "symbol": symbol,
            "extra_class": extra_class,
            "is_operator": "operator-node" in extra_class,
            "long_label": len(business_label) > 22 or len(developer_label) > 22,
        }

    def _formula_tokens_from_expression(expression: str, prefer_source_labels: bool = False) -> list[dict]:
        parts = _tokenize_formula_expression(expression)
        tokens: list[dict] = []
        idx = 0
        while idx < len(parts):
            part = parts[idx]
            if part in {"(", ")"}:
                idx += 1
                continue
            if part in {"+", "-", "/", "÷"}:
                business, developer, symbol = _operator_label(part)
                tokens.append(_formula_node_token(business, developer, symbol, " operator-node"))
                idx += 1
                continue
            if part in {"*", "×"}:
                next_part = parts[idx + 1] if idx + 1 < len(parts) else ""
                if re.fullmatch(r"\d+(?:\.\d+)?", next_part):
                    tokens.append(
                        _formula_node_token(
                            "Normalized Annual Days" if next_part == "365" else f"Scaled by {next_part}",
                            f"LITERAL: * {next_part}",
                            f"× {next_part}",
                            " operator-node",
                        )
                    )
                    idx += 2
                    continue
                business, developer, symbol = _operator_label(part)
                tokens.append(_formula_node_token(business, developer, symbol, " operator-node"))
                idx += 1
                continue
            if re.fullmatch(r"\d+(?:\.\d+)?", part):
                tokens.append(_formula_node_token(f"Literal {part}", f"LITERAL: {part}", part))
                idx += 1
                continue
            if prefer_source_labels:
                business_label = _business_label_for_code_token(part)
                mapping_kind = "VARIABLE" if (kpi_data.get("language") or "").lower() == "python" else "COLUMN"
                developer_label = f"{mapping_kind}: {part}"
                symbol = _math_symbol_for_token(part)
            else:
                developer_tokens = _developer_tokens_from_source()
                business_label = part
                developer_label = _developer_label_for(part, developer_tokens)
                symbol = _math_symbol_for_token(part)
            tokens.append(_formula_node_token(business_label, developer_label, symbol))
            idx += 1
        return tokens

    def _nodes_from_expression(expression: str, prefer_source_labels: bool = False) -> list[str]:
        return [
            _formula_node_html(
                token["business_label"],
                token["developer_label"],
                token["symbol"],
                token["extra_class"],
            )
            for token in _formula_tokens_from_expression(expression, prefer_source_labels)
        ]

    def _shorten_label(label: str, max_len: int = 34) -> str:
        text = re.sub(r"\s+", " ", label).strip()
        if len(text) <= max_len:
            return text
        return text[: max_len - 1].rstrip() + "…"

    def _annotated_equation_html() -> str:
        tokens = _annotated_equation_tokens()
        if not tokens:
            return ""
        return (
            '<div class="leap-annotated-formula-wrapper leap-annotated-equation" data-perspective="business">'
            + "".join(
                _formula_node_html(
                    token["business_label"],
                    token["developer_label"],
                    token["symbol"],
                    token["extra_class"],
                )
                for token in tokens
            )
            + "</div>"
        )

    def _annotated_equation_tokens() -> list[dict]:
        formula_text = _plain_text(formula_description_raw)
        source_expr = _fallback_annotation_expression()
        if not _looks_like_formula(formula_text):
            return _formula_tokens_from_expression(source_expr, prefer_source_labels=True)
        aggregate_match = re.match(
            r"(?is)^(?P<kind>sum|count|average)\s+of\s+(?:all\s+)?(?P<item>.+)$",
            formula_text,
        )
        if formula_mismatch:
            source_tokens = _formula_tokens_from_expression(source_expr, prefer_source_labels=True)
            if source_tokens:
                return source_tokens
        if aggregate_match:
            kind = aggregate_match.group("kind").title()
            item = aggregate_match.group("item").strip()
            developer_tokens = _developer_tokens_from_source()
            business_label = _shorten_label(item, 56)
            developer_label = _shorten_label(_developer_label_for(item, developer_tokens), 48)
            symbol = "Σ" if kind == "Sum" else ("avg" if kind == "Average" else "count")
            return [_formula_node_token(business_label, developer_label, symbol)]
        tokens = _formula_tokens_from_expression(formula_text, prefer_source_labels=False)
        operand_count = sum(1 for token in tokens if not token.get("is_operator"))
        return tokens if operand_count >= 2 else []

    def _normalize_formula_tokens(tokens: list[dict]) -> list[dict]:
        normalized: list[dict] = []
        for raw in tokens or []:
            if not isinstance(raw, dict):
                continue
            business_label = str(raw.get("business_label") or "").strip()
            developer_mapping = str(
                raw.get("developer_mapping") or raw.get("developer_label") or ""
            ).strip()
            math_symbol = str(raw.get("math_symbol") or raw.get("symbol") or "").strip()
            if not business_label or not developer_mapping or not math_symbol:
                continue
            token = _formula_node_token(
                business_label,
                developer_mapping,
                math_symbol,
                str(raw.get("extra_class") or (" operator-node" if raw.get("is_operator") else "")),
            )
            token["business_label"] = business_label
            token["developer_mapping"] = developer_mapping
            token["developer_label"] = developer_mapping
            token["math_symbol"] = math_symbol
            token["symbol"] = math_symbol
            token["is_operator"] = bool(raw.get("is_operator")) or "OPERATOR:" in developer_mapping
            token["long_label"] = len(business_label) > 22 or len(developer_mapping) > 22
            normalized.append(token)
        if not normalized:
            fallback_expr = _fallback_annotation_expression()
            fallback_label = _business_label_for_code_token(fallback_expr) if fallback_expr else (kpi_name or "Result")
            fallback_symbol = _math_symbol_for_token(fallback_expr) if fallback_expr else "Result"
            developer_mapping = UNMAPPED_DEVELOPER_LINEAGE
            token = _formula_node_token(fallback_label, developer_mapping, fallback_symbol)
            token["business_label"] = fallback_label
            token["developer_mapping"] = developer_mapping
            token["developer_label"] = developer_mapping
            token["math_symbol"] = fallback_symbol
            token["symbol"] = fallback_symbol
            token["long_label"] = len(fallback_label) > 22 or len(developer_mapping) > 22
            normalized.append(token)
        return normalized

    movement_up, movement_down = _movement_language(kpi_name)
    plain_meaning = _first_sentence(
        details.get("description", ""),
        f"{kpi_name or 'This KPI'} is a discovered performance indicator calculated from source-system logic.",
    )
    decision_support = _first_sentence(
        details.get("objective", ""),
        f"Supports review of {kpi_data['governance_domain_display'].lower()} performance, ownership, and follow-up actions.",
    )
    input_text = _plain_text(details.get("input_measure", ""))
    if not input_text:
        input_text = "Review the source evidence to confirm the exact fields, filters, and tables used."
    owner_logic = (
        f"If this KPI trends up: {movement_up} "
        f"If it trends down: {movement_down} "
        f"Owner check: What changed in source data, business process, or KPI logic that explains movement in {kpi_name or 'this KPI'}?"
    )

    def _walkthrough_operational_intent() -> str:
        meaning = _plain_text(plain_meaning)
        if meaning:
            return (
                f"{meaning} LEAP frames this as an operational evidence signal for "
                f"{kpi_data['governance_domain_display'].lower()} decision-making."
            )
        return (
            f"This metric exposes a measurable operating condition so {kpi_data['governance_domain_display'].lower()} "
            "leaders can compare performance, detect drift, and assign follow-up ownership."
        )

    def _walkthrough_recipe_html() -> str:
        formula = _plain_text(formula_description_raw) or _plain_text(final_details.get("formula_description", ""))
        source = kpi_data.get("source_file_display") or "the captured source file"
        language = kpi_data.get("source_language_display") or "SOURCE"
        steps = [
            f"First, LEAP anchors the KPI definition to {source} and classifies the implementation as {language} evidence.",
            f"Second, it translates the approved business expression ({formula or 'the captured source expression'}) into the formal MathJax formula shown above.",
            "Finally, it preserves the executable code context and code fingerprint so future changes to the KPI logic can be detected.",
        ]
        return "<ol>" + "".join(f"<li>{escape(step)}</li>" for step in steps) + "</ol>"

    def _walkthrough_safeguards_html() -> str:
        code_context = kpi_data.get("code_context") or ""
        safeguards: list[tuple[str, str]] = []
        if re.search(r"(?is)\bNULLIF\s*\(", code_context):
            safeguards.append(
                (
                    "Zero-Division Guard",
                    "Source logic uses NULLIF so denominator values of zero do not create invalid ratio calculations.",
                )
            )
        elif re.search(r"(?is)\bif\s*\(.+==\s*0\)|\bif\s+.+==\s*0", code_context):
            safeguards.append(
                (
                    "Zero-Division Guard",
                    "Source logic checks for a zero denominator before returning the KPI value.",
                )
            )
        else:
            safeguards.append(
                (
                    "Source Traceability",
                    f"Executable evidence is locked to {kpi_data.get('source_file_display') or 'the captured source file'} at line {kpi_data.get('source_line_number', 1)}.",
                )
            )
        if formula_mismatch:
            safeguards.append(
                (
                    "Governance Conflict Flag",
                    "LEAP detected that the documented business formula and source execution path disagree, so the KPI is explicitly flagged for owner review.",
                )
            )
        else:
            safeguards.append(
                (
                    "Formula Consistency Check",
                    "The business formula and source evidence share compatible calculation structure based on LEAP's static comparison.",
                )
            )
        safeguards.append(
            (
                "Change Detection",
                f"Code Fingerprint {kpi_data.get('code_hash', '')} records the current implementation so drift can be detected after regeneration.",
            )
        )
        if kpi_data.get("governance_accountable"):
            safeguards.append(
                (
                    "RACI Accountability",
                    f"{kpi_data['governance_accountable']} is assigned as accountable owner for rule confirmation and escalation.",
                )
            )
        return (
            '<div class="walkthrough-proof-list">'
            + "".join(
                '<div class="walkthrough-proof-item">'
                '<span class="walkthrough-check">OK</span>'
                f'<div><strong>{escape(title)}:</strong> {escape(body)}</div>'
                "</div>"
                for title, body in safeguards
            )
            + "</div>"
        )

    def _walkthrough_signoff() -> str:
        basis = kpi_data.get("governance_basis") or "local RACI governance rules"
        owner = kpi_data.get("governance_accountable") or "Domain Owner"
        consulted = kpi_data.get("governance_consulted") or "Domain SME"
        return (
            f"Business rules are aligned to {basis}. RACI Owner: {owner}. "
            f"Consulted reviewer: {consulted}. Current status: {'Needs Review' if formula_mismatch else 'Extracted for validation'}."
        )

    review_body = "\n".join(
        [
            "Please review this LEAP KPI evidence file.",
            "",
            f"KPI: {kpi_name or 'KPI'}",
            f"KPI ID: {kpi_data.get('kpi_identity_display', '')}",
            f"Accountable owner: {kpi_data.get('governance_accountable', '')}",
            f"Consulted SME: {kpi_data.get('governance_consulted', '')}",
            f"Source: {kpi_data.get('source_file_display', '')}",
            f"Line: {kpi_data.get('source_line_number', '')}",
            "",
            "Review questions:",
            "- Does the business meaning match how the KPI is used?",
            "- Does the formula reflect the approved business rule?",
            "- Are the source fields, filters, and reporting period correct?",
            "- Should this KPI be marked Validated or Needs Review?",
        ]
    )
    formula_tokens = _normalize_formula_tokens(_annotated_equation_tokens())
    kpi_data["formula_tokens"] = formula_tokens

    formula_is_undetermined = "UNDETERMINED" in str(formula_description_raw).upper()
    governance_confidence_text = str(kpi_data.get("governance_confidence") or "").strip().lower()
    manual_override_approved = (
        str(details.get("_override_status") or "").strip().upper()
        == "APPROVED_BY_BUSINESS"
    )
    try:
        numeric_confidence = float(kpi_data.get("confidence", 0) or 0)
    except (TypeError, ValueError):
        numeric_confidence = 0.0

    if formula_mismatch:
        review_state_label = "Needs Review"
        review_state_class = "state-needs-review"
        review_action_label = "Review Logic Mismatch"
        review_state_reason = formula_mismatch_reason
    elif manual_override_approved:
        review_state_label = "Validated"
        review_state_class = "state-validated"
        review_action_label = "Review Approved Override"
        review_state_reason = (
            "This KPI uses a business-approved override from the LEAP AXIS sign-off ledger. "
            "The saved definition is applied before dossier rendering."
        )
    elif formula_is_undetermined or not formula_tokens or numeric_confidence < 75 or governance_confidence_text == "low":
        review_state_label = "Needs Review"
        review_state_class = "state-needs-review"
        review_action_label = "Review Extraction"
        review_state_reason = (
            "LEAP extracted the KPI candidate, but the formula, lineage tokens, or governance confidence "
            "requires owner confirmation before the dossier is treated as reliable."
        )
    else:
        review_state_label = "Extracted"
        review_state_class = "state-extracted"
        review_action_label = "Review Evidence"
        review_state_reason = (
            "LEAP extracted the KPI and mapped governance metadata. Human validation is still required "
            "before this KPI should be marked as formally approved."
        )

    final_details.update(
        {
            "business_plain_meaning": escape(plain_meaning),
            "business_decision_support": escape(decision_support),
            "business_moves_up": escape(movement_up),
            "business_moves_down": escape(movement_down),
            "business_owner_logic": escape(owner_logic),
            "business_owner_question": escape(
                f"What changed in source data, business process, or KPI logic that explains movement in {kpi_name or 'this KPI'}?"
            ),
            "review_mailto": "mailto:?"
            + urlencode(
                {
                    "subject": f"LEAP KPI review requested: {kpi_name or 'KPI'}",
                    "body": review_body,
                }
            ),
            "review_body": escape(review_body),
            "review_body_textarea": escape(review_body).replace("\n", "&#10;"),
            "business_formula": escape(_business_formula_sentence()),
            "formula_tokens": formula_tokens,
            "annotated_equation_html": _annotated_equation_html(),
            "developer_lineage_html": _developer_lineage_html(),
            # Add LaTeX formula HTML if detected
            "formula_html": latex_formula_html,
            # Backwards-compatible flag used in some templates
            "has_governance_mismatch": bool(formula_mismatch),
            # New ISO-focused conflict flag for templates and styling
            "iso_governance_conflict": bool(formula_mismatch),
            # Human-readable reason (now prefixed with ISO label when applicable)
            "governance_mismatch_reason": escape(formula_mismatch_reason),
            "review_state_label": escape(review_state_label),
            "review_state_class": review_state_class,
            "review_action_label": escape(review_action_label),
            "review_state_reason": escape(review_state_reason),
            "walkthrough_operational_intent": escape(_walkthrough_operational_intent()),
            "walkthrough_recipe_html": _walkthrough_recipe_html(),
            "walkthrough_safeguards_html": _walkthrough_safeguards_html(),
            "walkthrough_signoff": escape(_walkthrough_signoff()),
            "evidence_snippet": escape(_evidence_snippet()),
        }
    )
    fields_to_check = [
        "description_html",
        "objective_html",
        "formula_description",
        "used_in_kpis_html",
        "input_measure_html",
        "unit_of_measure",
        "reporting_source",
        "comments",
    ]

    def _non_empty(val: str | None) -> bool:
        if not isinstance(val, str):
            return False
        s = val.strip()
        if len(s) <= 2:
            return False
        return not re.fullmatch(r"[\s\W_]*", s)

    filled = sum(1 for k in fields_to_check if _non_empty(final_details.get(k)))
    formula_html = final_details.get("formula_html") or ""
    formula_is_specific = bool(formula_html) and (
        "See code context" not in formula_html
    )
    filled_total = filled + (1 if formula_is_specific else 0)
    possible_total = len(fields_to_check) + 1
    extraction_rate_pct = round(100.0 * filled_total / possible_total, 1)
    error_rate_pct = round(100.0 - extraction_rate_pct, 1)
    final_details["extraction_rate_pct"] = extraction_rate_pct
    final_details["error_rate_pct"] = error_rate_pct

    def _fmt_seconds(s: float) -> str:
        s = max(0.0, float(s))
        if s < 60:
            return f"{s:.1f}s"
        m = int(s // 60)
        r = int(round(s - m * 60))
        return f"{m}m {r}s"

    render_time_seconds = time.perf_counter() - render_start
    total_kpi_time_seconds = (ai_time_seconds or 0.0) + render_time_seconds
    final_details["ai_time_seconds"] = round(ai_time_seconds or 0.0, 3)
    final_details["render_time_seconds"] = round(render_time_seconds, 3)
    final_details["total_kpi_time_seconds"] = round(total_kpi_time_seconds, 3)
    final_details["generation_time_display"] = (
        f"{_fmt_seconds(total_kpi_time_seconds)} "
        f"(Details {_fmt_seconds(ai_time_seconds or 0.0)} + Render {_fmt_seconds(render_time_seconds)})"
    )
    explicit_formula = kpi_data.get("formula")
    if explicit_formula:
        final_details["formula_html"] = (
            f'<div class="math-equation">$$ {explicit_formula} $$</div>'
        )
    safe_name = "".join(
        c for c in (kpi_name or "") if c.isalnum() or c in (" ", "_")
    ).rstrip()
    base_filename = (safe_name.replace(" ", "_").lower() or "kpi") + ".rst"
    reserved_filenames = {"index.rst", "conf.rst", "genindex.rst", "search.rst"}
    filename = base_filename
    output_path = DOCS_SOURCE_DIR / filename
    if filename in reserved_filenames or output_path.exists():
        source_hint = str(kpi_data.get("file_path") or kpi_name or filename)
        digest = hashlib.md5(source_hint.encode("utf-8")).hexdigest()[:8]
        stem, suffix = os.path.splitext(base_filename)
        if base_filename in reserved_filenames:
            stem = f"kpi_{stem}"
        filename = f"{stem}_{digest}{suffix or '.rst'}"
        output_path = DOCS_SOURCE_DIR / filename
    content = template.render(kpi=kpi_data, details=final_details)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return filename


def _confidence_band(confidence: float) -> str:
    try:
        value = float(confidence)
    except Exception:
        value = 0.0
    if value >= 85:
        return "High"
    if value >= 65:
        return "Medium"
    return "Low"


def _slug_for_ref(text: str) -> str:
    s = (text or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "kpi"


def create_discovery_report(
    kpis: list[dict],
    page_filenames: list[str],
    source_code_path: str,
    scan_stats: dict,
    ai_wall: float,
) -> str:
    from collections import Counter, defaultdict

    report_name = "discovery_report.rst"
    report_path = DOCS_SOURCE_DIR / report_name
    paired = list(zip(kpis, page_filenames))
    total = len(kpis)
    confidence_counts = Counter(_confidence_band(k.get("confidence", 0)) for k in kpis)
    language_counts = Counter((k.get("language") or "unknown").lower() for k in kpis)
    kind_counts = Counter(
        str(k.get("detection_kind") or k.get("_kind") or "unspecified")
        for k in kpis
    )
    accountable_counts = Counter(
        ((k.get("governance") or {}).get("accountable") or "Unassigned") for k in kpis
    )
    governance_method_counts = Counter(
        ((k.get("governance") or {}).get("method") or "Unspecified") for k in kpis
    )
    by_name = defaultdict(list)
    for k, page in paired:
        by_name[(k.get("name") or "KPI").strip().lower()].append((k, page))
    duplicates = {
        name: entries for name, entries in by_name.items() if len(entries) > 1
    }

    def source_display(k: dict) -> str:
        path = k.get("file_path") or ""
        if not path:
            return ""
        try:
            return str(Path(path).expanduser().resolve().relative_to(Path(source_code_path).expanduser().resolve()))
        except Exception:
            return str(path)

    lines = [
        "KPI Discovery Report",
        "====================",
        "",
        "Scan Overview",
        "-------------",
        "",
        ".. list-table::",
        "   :header-rows: 0",
        "   :widths: 35 65",
        "",
        f"   * - Source folder",
        f"     - ``{source_code_path}``",
        f"   * - All filesystem items found",
        f"     - {int(scan_stats.get('filesystem_items', 0)):,}",
        f"   * - All filesystem files found",
        f"     - {int(scan_stats.get('filesystem_files', 0)):,}",
        f"   * - All filesystem directories found",
        f"     - {int(scan_stats.get('filesystem_dirs', 0)):,}",
        f"   * - Files after directory exclusions",
        f"     - {int(scan_stats.get('files_after_directory_exclusions', 0)):,}",
        f"   * - Source files selected for KPI scan",
        f"     - {int(scan_stats.get('files_scanned', 0)):,}",
        f"   * - Binary/image files skipped",
        f"     - {int(scan_stats.get('skipped_binary_files', 0)):,}",
        f"   * - Unsupported files skipped",
        f"     - {int(scan_stats.get('unsupported_files', 0)):,}",
        f"   * - Non-KPI candidates filtered",
        f"     - {int(scan_stats.get('filtered_non_kpi_candidates', 0)):,}",
        f"   * - Ignored files skipped",
        f"     - {int(scan_stats.get('ignored_files', 0)):,}",
        f"   * - Ignored directories skipped",
        f"     - {int(scan_stats.get('ignored_dirs', 0)):,}",
        f"   * - Lines analyzed",
        f"     - {int(scan_stats.get('lines_analyzed', 0)):,}",
        f"   * - KPIs detected",
        f"     - {total:,}",
        f"   * - Compliance detail phase wall time",
        f"     - {ai_wall:.2f}s",
        "",
        "Confidence Summary",
        "------------------",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 40 20 40",
        "",
        "   * - Band",
        "     - Count",
        "     - Meaning",
        f"   * - High",
        f"     - {confidence_counts.get('High', 0):,}",
        "     - Explicit KPI marker, measure, or strong domain pattern",
        f"   * - Medium",
        f"     - {confidence_counts.get('Medium', 0):,}",
        "     - Useful candidate; review formula/context",
        f"   * - Low",
        f"     - {confidence_counts.get('Low', 0):,}",
        "     - Weak candidate; manual validation recommended",
        "",
        "Languages Detected",
        "------------------",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 50 50",
        "",
        "   * - Language",
        "     - KPI Count",
    ]
    for lang, count in sorted(language_counts.items(), key=lambda item: (-item[1], item[0])):
        lines += [f"   * - {lang}", f"     - {count:,}"]

    lines += [
        "",
        "Detection Methods",
        "-----------------",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 50 50",
        "",
        "   * - Method",
        "     - KPI Count",
    ]
    for kind, count in sorted(kind_counts.items(), key=lambda item: (-item[1], item[0])):
        lines += [f"   * - {kind.replace('_', ' ').title()}", f"     - {count:,}"]

    lines += [
        "",
        "Governance Summary",
        "------------------",
        "",
        ".. list-table:: Assignment Method",
        "   :header-rows: 1",
        "   :widths: 60 40",
        "",
        "   * - Method",
        "     - KPI Count",
    ]
    for method, count in sorted(governance_method_counts.items(), key=lambda item: (-item[1], item[0])):
        lines += [f"   * - {method}", f"     - {count:,}"]

    lines += [
        "",
        ".. list-table:: Accountable Owner",
        "   :header-rows: 1",
        "   :widths: 60 40",
        "",
        "   * - Accountable Owner",
        "     - KPI Count",
    ]
    for owner, count in sorted(accountable_counts.items(), key=lambda item: (-item[1], item[0])):
        lines += [f"   * - {owner}", f"     - {count:,}"]

    lines += [
        "",
        "Possible Duplicate KPI Names",
        "----------------------------",
        "",
    ]
    if duplicates:
        lines += [
            ".. list-table::",
            "   :header-rows: 1",
            "   :widths: 30 70",
            "",
            "   * - KPI Name",
            "     - Source Pages",
        ]
        for _, entries in sorted(duplicates.items(), key=lambda item: item[0]):
            display_name = entries[0][0].get("name") or "KPI"
            refs = []
            for k, page in entries:
                stem = os.path.splitext(os.path.basename(page))[0]
                refs.append(f":doc:`{stem}` ({source_display(k)})")
            lines += [f"   * - {display_name}", f"     - {'; '.join(refs)}"]
    else:
        lines += ["No duplicate KPI names were detected.", ""]

    lines += [
        "",
        "KPI Inventory",
        "-------------",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 24 10 10 18 18 20",
        "",
        "   * - KPI",
        "     - Confidence",
        "     - Language",
        "     - Detection",
        "     - Accountable",
        "     - Source",
    ]
    for k, page in paired:
        stem = os.path.splitext(os.path.basename(page))[0]
        governance = k.get("governance") or {}
        lines += [
            f"   * - :doc:`{stem}`",
            f"     - {float(k.get('confidence', 0) or 0):.0f}%",
            f"     - {(k.get('language') or 'unknown').upper()}",
            f"     - {str(k.get('detection_kind') or k.get('_kind') or 'unspecified').replace('_', ' ').title()}",
            f"     - {governance.get('accountable') or 'Unassigned'}",
            f"     - ``{source_display(k)}``",
        ]

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_name


def create_raci_directory(kpis: list[dict]) -> str:
    from collections import defaultdict
    from html import escape

    directory_name = "raci_directory.rst"
    directory_path = DOCS_SOURCE_DIR / directory_name
    stakeholder_kpis: dict[tuple[str, str], set[str]] = defaultdict(set)
    stakeholder_roles: dict[tuple[str, str], set[str]] = defaultdict(set)

    role_map = [
        ("Responsible", "responsible"),
        ("Accountable", "accountable"),
        ("Consulted", "consulted"),
        ("Informed", "informed"),
    ]
    for kpi in kpis:
        governance = kpi.get("governance") or {}
        kpi_name = kpi.get("name") or "KPI"
        for role_label, role_key in role_map:
            person = str(governance.get(role_key) or "").strip()
            if not person:
                continue
            key = (person, role_label)
            stakeholder_kpis[key].add(kpi_name)
            stakeholder_roles[key].add(role_label)

    def _slug(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", ".", value.lower()).strip(".") or "stakeholder"

    def _employee_id(name: str, role: str) -> str:
        digest = hashlib.md5(f"{name}:{role}".encode("utf-8")).hexdigest()[:6].upper()
        return f"LEAP-{digest}"

    def _email(name: str) -> str:
        return f"{_slug(name)}@enterprise.example"

    def _role_tier(role: str) -> str:
        return {
            "Accountable": "Decision Owner",
            "Responsible": "Execution Owner",
            "Consulted": "Subject Matter Reviewer",
            "Informed": "Executive Observer",
        }.get(role, "Governance Participant")

    rows = sorted(
        stakeholder_kpis.items(),
        key=lambda item: (item[0][1], item[0][0].lower()),
    )

    table_rows = []
    for (name, role), assigned in rows:
        badge_class = {
            "Responsible": "raci-r",
            "Accountable": "raci-a",
            "Consulted": "raci-c",
            "Informed": "raci-i",
        }.get(role, "raci-i")
        assigned_preview = ", ".join(sorted(assigned)[:5])
        if len(assigned) > 5:
            assigned_preview += f" + {len(assigned) - 5} more"
        table_rows.append(
            "<tr>"
            f"<td><strong>{escape(name)}</strong></td>"
            f"<td><code>{escape(_email(name))}</code></td>"
            f"<td><code>{escape(_employee_id(name, role))}</code></td>"
            f"<td>{escape(assigned_preview or 'No KPI assigned')}</td>"
            f'<td><span class="raci-badge {badge_class}">{escape(role[:1])}</span>{escape(_role_tier(role))}</td>'
            "</tr>"
        )

    html = f"""
<section class="raci-directory-admin">
  <div class="raci-directory-form">
    <div>
      <div class="micro-label">Governance Provisioning</div>
      <h2>Stakeholder Administration</h2>
      <p>Provision owners, reviewers, and informed stakeholders into the KPI governance matrix. This form is an interface scaffold for the offline governance registry.</p>
    </div>
    <form class="raci-provision-form">
      <label>
        <span>Employee Name</span>
        <input type="text" placeholder="e.g. Finance Data Owner">
      </label>
      <label>
        <span>Corporate Email</span>
        <input type="email" placeholder="name@enterprise.example">
      </label>
      <label>
        <span>Employee ID No</span>
        <input type="text" placeholder="LEAP-000000">
      </label>
      <label>
        <span>Role Tier</span>
        <select>
          <option>Accountable</option>
          <option>Responsible</option>
          <option>Consulted</option>
          <option>Informed</option>
        </select>
      </label>
      <button type="button">Provision Stakeholder</button>
    </form>
  </div>

  <div class="raci-directory-table-wrap">
    <table class="raci-directory-table">
      <thead>
        <tr>
          <th>Employee Name</th>
          <th>Corporate Email</th>
          <th>Employee ID No</th>
          <th>Assigned KPIs</th>
          <th>Role Tier</th>
        </tr>
      </thead>
      <tbody>
        {''.join(table_rows)}
      </tbody>
    </table>
  </div>
</section>
"""

    lines = [
        "RACI Stakeholder Directory",
        "==========================",
        "",
        ".. raw:: html",
        "",
    ]
    lines.extend(f"   {line}" if line else "" for line in html.strip().splitlines())
    directory_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return directory_name


def update_index_rst(page_filenames):
    index_path = DOCS_SOURCE_DIR / "index.rst"
    title = "KPI Bluebook"
    audit_stems = []
    kpi_stems = []
    for fname in page_filenames or []:
        if not fname:
            continue
        try:
            base = os.path.basename(str(fname))
            stem = os.path.splitext(base)[0]
            if not stem:
                continue
            if stem in {"discovery_report", "raci_directory"}:
                audit_stems.append(stem)
            else:
                kpi_stems.append(stem)
        except Exception:
            continue

    lines = [
        title,
        "=" * len(title),
        "",
        "Discovery & Audits",
        "------------------",
        "",
        "* **Code Scans**: source coverage, language mix, detection methods, and scan geometry.",
        "* **Extraction History**: generated Bluebook state, confidence bands, and publication outputs.",
        "* **Mismatch Reports**: governance exceptions where business formulas and executable code diverge.",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "   :caption: Discovery & Audits:",
        "",
    ]
    if audit_stems:
        lines.extend(f"   {stem}" for stem in audit_stems)
        lines.append("")

    lines.extend(
        [
            "Key Performance Indicators",
            "--------------------------",
            "",
            ".. toctree::",
            "   :maxdepth: 1",
            "   :caption: Key Performance Indicators:",
            "",
        ]
    )
    lines.extend(f"   {stem}" for stem in kpi_stems)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_bluebook(source_code_path: str, ground_truth_path: str = None):
    run_start = time.perf_counter()
    build_dir = DOCS_SOURCE_DIR / "_build"
    if build_dir.exists():
        shutil.rmtree(build_dir, ignore_errors=True)
        yield "Removed previous Sphinx _build directory."
    for item in DOCS_SOURCE_DIR.glob("*.rst"):
        if item.is_file() and item.name != "index.rst":
            item.unlink()
    yield "Cleaned old documentation files."
    yield f"Scanning for KPIs in: {source_code_path}"
    kpis, scan_stats = find_kpis_in_directory(source_code_path, include_stats=True)
    files_scanned = int(scan_stats.get("files_scanned", 0))
    lines_analyzed = int(scan_stats.get("lines_analyzed", 0))
    skipped_files = int(scan_stats.get("skipped_binary_files", 0))
    filesystem_files = int(scan_stats.get("filesystem_files", 0))
    filesystem_dirs = int(scan_stats.get("filesystem_dirs", 0))
    filesystem_items = int(scan_stats.get("filesystem_items", 0))
    files_after_dir_exclusions = int(scan_stats.get("files_after_directory_exclusions", 0))
    yield (
        f"Scanner result: {len(kpis)} KPI candidates "
        f"(all files: {filesystem_files}, post-directory-exclusion files: {files_after_dir_exclusions}, "
        f"source files selected: {files_scanned})"
    )
    attach_governance(kpis, ROOT_DIR, DOCS_SOURCE_DIR)
    yield "Governance layer: assigned RACI ownership using local rules and overrides."
    definition_overrides = _load_definition_overrides()
    if definition_overrides:
        yield f"Definition override ledger: loaded {len(definition_overrides)} approved override entries."
    if not kpis:
        yield "No KPIs found in the specified directory."
        return
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)))
    try:
        template = env.get_template("kpi_template.rst.j2")
    except Exception:
        template = env.from_string(
            "{{ kpi.name }}\n{{ '=' * (kpi.name|length) }}\n\n"
            ".. raw:: html\n\n   {{ details.formula_html|safe }}\n\n"
            ".. admonition:: Code Context\n   :class: dropdown\n\n"
            "   .. code-block:: text\n      :linenos:\n\n"
            "      {{ kpi.code_context | e }}\n"
        )

    def _trim_context(kpi: dict, max_lines: int = 120, around: int = 60) -> str:
        ctx = kpi.get("code_context", "")
        line_no = int(kpi.get("file_line") or 0)
        lines = ctx.splitlines()
        if not lines:
            return ctx
        if 1 <= line_no <= len(lines):
            start = max(0, line_no - around - 1)
            end = min(len(lines), line_no + around)
            return "\n".join(lines[start:end])
        return "\n".join(lines[:max_lines])

    def _ai_task(k):
        name = k.get("name") or "KPI"
        t0 = time.perf_counter()
        try:
            trimmed = _trim_context(k)
            if len(trimmed) > 6000:
                trimmed = trimmed[:3000] + "\n...\n" + trimmed[-3000:]
            details = generate_kpi_details(name, trimmed)
            details = _apply_definition_override(k, details, definition_overrides)
            ai_time = time.perf_counter() - t0
            return (k, details, ai_time, None)
        except Exception as e:
            fallback = {
                "description": f'SOURCE-VERIFIED CANDIDATE: LEAP detected calculation logic named "{name}" in the scanned source. No business meaning was inferred beyond the source text.',
                "objective": "UNDETERMINED: No explicit business objective found in source file.",
                "formula_description": "UNDETERMINED: No approved business formula statement found in source comments.",
                "used_in_kpis": "UNDETERMINED: No dashboard, report, or business-process usage mapping found in source file.",
                "input_measure": "UNDETERMINED: No explicit input-field list found in source file.",
                "unit_of_measure": "UNDETERMINED: No explicit unit of measure found in source file.",
                "reporting_source": "LINEAGE UNDETERMINED: No explicit database schema or variable mapping found in source file.",
                "comments": "Strict compliance mode: detail generation failed, so LEAP preserved only source-grounded uncertainty statements.",
            }
            fallback = _apply_definition_override(k, fallback, definition_overrides)
            return (k, fallback, 0.0, e)

    max_workers = int(os.environ.get("KPI_AI_WORKERS", "4"))
    results = []
    yield f"Compliance detail phase: processing {len(kpis)} KPIs with {max_workers} workers..."
    ai_phase_start = time.perf_counter()
    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        future_map = {ex.submit(_ai_task, k): k for k in kpis}
        for fut in as_completed(future_map):
            k, details, ai_time, err = fut.result()
            name = k.get("name") or "KPI"
            if err:
                yield f"Compliance detail generation failed for '{name}': {err}"
            else:
                yield f"Compliance details ready for '{name}' ({ai_time:.2f}s)."
            results.append((k, details, ai_time))
    ai_wall = time.perf_counter() - ai_phase_start
    page_files = []
    rendered_kpis = []
    for k, details, ai_time in results:
        name = k.get("name") or "KPI"
        try:
            k["source_root"] = source_code_path
            page = create_rst_file(k, details, template, ai_time_seconds=ai_time)
            page_files.append(page)
            rendered_kpis.append(k)
            yield f"Rendered '{name}'."
        except Exception as e:
            yield f"Failed to render page for '{name}': {e}"
    if results:
        total_ai = sum(ai for _, _, ai in results)
        avg_ai = total_ai / len(results)
        avg_wall_per_kpi = ai_wall / len(results)
        yield f"Compliance detail phase wall time: {ai_wall:.2f}s for {len(results)} KPIs with {max_workers} workers."
        yield f"Detail generation latency (sum across KPIs): {total_ai:.2f}s; avg per KPI latency: {avg_ai:.2f}s; avg wall time per KPI (wall/num): {avg_wall_per_kpi:.2f}s"
    total_conf = sum(k.get("confidence", 0) for k in kpis)
    avg_conf = total_conf / len(kpis) if kpis else 0
    false_positives = None
    false_negatives = None
    if ground_truth_path and os.path.exists(ground_truth_path):
        try:
            with open(ground_truth_path, "r", encoding="utf-8") as f:
                ground_truth = set(line.strip() for line in f if line.strip())
            extracted_names = {k.get("name") for k in kpis if k.get("name")}
            false_positives = len(extracted_names - ground_truth)
            false_negatives = len(ground_truth - extracted_names)
        except Exception as e:
            yield f"Warning: could not load ground truth: {e}"
    yield "=" * 70
    yield "📊 SCAN SUMMARY"
    yield f"All filesystem items found: {filesystem_items:,}"
    yield f"All filesystem files found: {filesystem_files:,}"
    yield f"All filesystem directories found: {filesystem_dirs:,}"
    yield f"Files after directory exclusions: {files_after_dir_exclusions:,}"
    yield f"Source files selected for KPI scan: {files_scanned:,}"
    yield f"Binary/image files skipped: {skipped_files:,}"
    yield f"Unsupported files skipped: {int(scan_stats.get('unsupported_files', 0)):,}"
    yield f"Non-KPI candidates filtered: {int(scan_stats.get('filtered_non_kpi_candidates', 0)):,}"
    yield f"Ignored files skipped: {int(scan_stats.get('ignored_files', 0)):,}"
    yield f"Ignored directories skipped: {int(scan_stats.get('ignored_dirs', 0)):,}"
    yield f"Lines of code analyzed: {lines_analyzed:,}"
    yield f"KPIs detected: {len(kpis)}"
    yield f"KPIs extracted: {len(kpis)}"
    if false_positives is not None:
        yield f"False positives: {false_positives}"
        yield f"False negatives: {false_negatives}"
    else:
        yield "False positives: N/A (ground truth not provided)"
        yield "False negatives: N/A (ground truth not provided)"
    yield f"Average confidence: {avg_conf:.1f}%"
    yield "=" * 70
    try:
        report_page = create_discovery_report(
            rendered_kpis,
            page_files,
            source_code_path,
            scan_stats,
            ai_wall,
        )
        raci_page = create_raci_directory(rendered_kpis)
        update_index_rst([report_page, raci_page] + page_files)
        yield f"Updated index.rst with discovery report, RACI directory, and {len(page_files)} KPI entries."
    except Exception as e:
        yield f"Failed to update index.rst: {e}"
    try:
        if os.environ.get("SKIP_SPHINX"):
            yield "Skipped sphinx-build (SKIP_SPHINX set)."
        else:
            jobs = os.environ.get("SPHINX_JOBS", "auto")
            cp = subprocess.run(
                [
                    "sphinx-build",
                    "-j",
                    jobs,
                    "-b",
                    "html",
                    str(DOCS_SOURCE_DIR),
                    str(DOCS_SOURCE_DIR / "_build"),
                ],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if cp.returncode == 0:
                yield "Sphinx build successful."
            else:
                err = (cp.stderr or b"").decode("utf-8", errors="ignore")
                yield f"Sphinx build finished with code {cp.returncode}.\n{err[:500]}"
    except Exception as e:
        yield f"sphinx-build not run: {e}"
    total_wall = time.perf_counter() - run_start
    yield f"Total wall time: {total_wall:.2f}s"
