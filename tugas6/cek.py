import sys
from pathlib import Path
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
JS = Language(tsjavascript.language())

CONFIG = {
    ".py": (
        Parser(PY),
        Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))'),
        Query(PY, "(function_definition name: (identifier) @nama) @fungsi"),
    ),
    ".js": (
        Parser(JS),
        Query(JS, '((comment) @c (#match? @c "TODO|FIXME"))'),
        Query(
            JS,
            """
            [
              (function_declaration name: (identifier) @nama) @fungsi
              (method_definition name: (property_identifier) @nama) @fungsi
              (variable_declarator
                name: (identifier) @nama
                value: [(arrow_function) (function_expression)]) @fungsi
            ]
            """,
        ),
    ),
}

SKIP_DIRS = {"venv", ".venv", ".git", "__pycache__", "node_modules"}


def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        err = cari_error(child)
        if err:
            return err
    return None


def cek_file(path: Path):
    if path.suffix not in CONFIG:
        return

    parser, q_todo, q_fungsi = CONFIG[path.suffix]
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(q_todo).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, captures in QueryCursor(q_fungsi).matches(tree.root_node):
        fn_node = captures["fungsi"][0]
        nama_node = captures["nama"][0]
        jumlah_baris = fn_node.end_point[0] - fn_node.start_point[0] + 1
        if jumlah_baris > 30:
            nama = nama_node.text.decode(errors="replace")
            print(f"{path}:{fn_node.start_point[0] + 1}: fungsi '{nama}' terlalu panjang ({jumlah_baris} baris)")

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        err = cari_error(tree.root_node)
        baris = err.start_point[0] + 1 if err else 1
        print(f"{path}:{baris}: error sintaks pada pohon parse")


for path in sorted(Path(sys.argv[1]).rglob("*")):
    if path.is_file() and not any(part in SKIP_DIRS for part in path.parts):
        cek_file(path)