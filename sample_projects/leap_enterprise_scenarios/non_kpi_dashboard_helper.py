def render_status_card(title: str, value: str) -> str:
    return f"<section><h2>{title}</h2><strong>{value}</strong></section>"


def visit_decoration(node) -> None:
    node["decorated"] = True
