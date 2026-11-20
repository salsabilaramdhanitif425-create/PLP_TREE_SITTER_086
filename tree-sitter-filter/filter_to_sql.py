import re
import tree_sitter_filter
from tree_sitter import Language, Parser

FILTER_LANGUAGE = Language(tree_sitter_filter.language())
PARSER = Parser(FILTER_LANGUAGE)
VALID_IDENTIFIER = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_.]*$")


def _text(node, source: bytes) -> str:
    return source[node.start_byte:node.end_byte].decode("utf-8")


def _extract_identifier(node, source: bytes) -> str:
    col = _text(node, source)
    if not VALID_IDENTIFIER.match(col):
        raise ValueError(f"Nama kolom tidak valid: {col!r}")
    return col


def _extract_value(node, source: bytes):
    raw = _text(node, source)
    if node.type == "string":
        return raw[1:-1]  # hapus tanda kutip ganda di awal dan akhir
    if node.type == "number":
        return float(raw) if "." in raw else int(raw)
    if node.type == "boolean":
        return raw == "true"
    raise ValueError(f"Tipe nilai tidak dikenal: {node.type}")


def _visit(node, source: bytes) -> tuple[str, list]:
    t = node.type

    if t == "query":
        if not node.named_children:
            raise ValueError("Query kosong.")
        return _visit(node.named_children[0], source)

    if t == "parenthesized":
        inner_sql, inner_params = _visit(node.named_children[0], source)
        return f"({inner_sql})", inner_params

    if t == "and_expression":
        left_sql, left_params = _visit(node.child_by_field_name("left"), source)
        right_sql, right_params = _visit(node.child_by_field_name("right"), source)
        return f"({left_sql} AND {right_sql})", left_params + right_params

    if t == "or_expression":
        left_sql, left_params = _visit(node.child_by_field_name("left"), source)
        right_sql, right_params = _visit(node.child_by_field_name("right"), source)
        return f"({left_sql} OR {right_sql})", left_params + right_params

    if t == "not_expression":
        op_sql, op_params = _visit(node.child_by_field_name("operand"), source)
        return f"NOT ({op_sql})", op_params

    if t == "comparison":
        col = _extract_identifier(node.child_by_field_name("left"), source)
        op = _text(node.child_by_field_name("operator"), source)
        val = _extract_value(node.child_by_field_name("right"), source)
        return f"{col} {op} ?", [val]

    if t == "in_expression":
        col = _extract_identifier(node.child_by_field_name("left"), source)
        list_node = node.child_by_field_name("right")
        values = [_extract_value(child, source) for child in list_node.named_children]
        if not values:
            return "1 = 0", []
        placeholders = ", ".join(["?"] * len(values))
        return f"{col} IN ({placeholders})", values

    if t == "contains_expression":
        col = _extract_identifier(node.child_by_field_name("left"), source)
        substr = _extract_value(node.child_by_field_name("right"), source)
        escaped = substr.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        return f"{col} LIKE ?", [f"%{escaped}%"]

    raise ValueError(f"Node tidak didukung: {t}")


def filter_to_sql(dsl_query: str) -> tuple[str, list]:
    source = dsl_query.encode("utf-8")
    tree = PARSER.parse(source)
    if tree.root_node.has_error:
        raise SyntaxError(f"Sintaks filter tidak valid: {dsl_query!r}")
    where_body, params = _visit(tree.root_node, source)
    return f"WHERE {where_body}", params


if __name__ == "__main__":
    contoh_queries = [
        'status = "open" and priority >= 2',
        '(role = "admin" or role = "editor") and not archived = true',
        'status in ("open", "pending") and title contains "invoice"',
    ]

    for q in contoh_queries:
        sql, params = filter_to_sql(q)
        print(f"DSL   : {q}")
        print(f"SQL   : {sql}")
        print(f"Params: {params}")
        print("-" * 60)