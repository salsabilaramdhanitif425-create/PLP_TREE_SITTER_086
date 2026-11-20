import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode_fungsi = b"""def tambah_satu(n):
    return n + 1
"""

kode_if_else = b"""if nilai >= 75:
    status = "lulus"
else:
    status = "ulang"
"""
kode_kelas = b"""class Persegi:
    def luas(self, sisi):
        return sisi * sisi
"""

print("=== FUNGSI ===")
tree = parser.parse(kode_fungsi)
print(tree.root_node)

print("\n=== IF/ELSE ===")
tree_if = parser.parse(kode_if_else)               
print(tree_if.root_node)

print("\n=== KELAS ===")
tree_kelas = parser.parse(kode_kelas)          
print(tree_kelas.root_node)

print("\n=== CEK NODE ANONIM (FUNGSI) ===")
tree_fungsi = parser.parse(kode_fungsi)
fn_node = tree_fungsi.root_node.children[0]
for c in fn_node.children:                                      #menelusuri seluruh anak node fungsi (termasuk token anonim)
    print(c.type, "-> bernama" if c.is_named else "-> anonim")  #membedakan node aturan grammar vs token literal

params_node = fn_node.child_by_field_name("parameters")         #mengambil node bagian parameter berdasarkan nama field-nya
for c in params_node.children:                                  #menelusuri token yg ada di dalam kurung parameter
    print(" ", c.type, "-> bernama" if c.is_named else "-> anonim")

print("\n=== UJI ERROR / MISSING ===")
kode_rusak = b"""def tambah_satu(n)
    return n + 1
"""

tree_rusak = parser.parse(kode_rusak)  #mem-parse kode yang titik duanya hilang untuk melihat cara parser menangani kesalahan
print(tree_rusak.root_node)            #mencetak pohon hasil parse untuk mencari dimana node yg ERROR atau MISSING