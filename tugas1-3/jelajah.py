import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    # TODO: untuk setiap child yang bernama, panggil jelajah() lagi
    #       dengan kedalaman + 1 dan nama field-nya.
    
    for i, child in enumerate(node.children):      #menelusuri semua anak node beserta nomor urut (indeks) aslinya
        if not child.is_named:                     #melewati token anonim (seperti '=', '(', ':') agar tidak tercetak
            continue
        nama_field = node.field_name_for_child(i)  #mengecek apakah anak di indeks ke-i punya label peran (misal: left/right)
        jelajah(child, kedalaman + 1, nama_field)  #memanggil fungsi ini untuk anak node dengan kedalamanya bertambah 1

with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah(tree.root_node)