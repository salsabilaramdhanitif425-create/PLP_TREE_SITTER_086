import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)
cursor = QueryCursor(Query(PY, pola))

if "@params" in pola:                                                           
        if "nama" in cap and "params" in cap:
            nama = cap["nama"][0].text.decode()
            jumlah = cap["params"][0].named_child_count
            print(f"{nama}: {jumlah} parameter")
else:                                                                           
    for nama, nodes in cursor.captures(tree.root_node).items():
        if nama.startswith("_"):                                                
            continue
        for n in nodes:
            print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode()}")