import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))  

def jelajah_cursor(tree):
    cursor = tree.walk()                        #membuat penunjuk (cursor) yang berdiri di node paling atas (module)
    kedalaman = 0
    selesai = False

    while not selesai:
        node = cursor.node                      #mengambil node tempat dimana cursor berdiri saat ini
        if node.is_named:                       #hanya mencetak node bernama (token yg anonim dilewati)
            baris, kolom = node.start_point
            field = cursor.field_name           #mengambil nama field node saat ini langsung dari cursor
            label = f"{field}: " if field else ""
            print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

        if cursor.goto_first_child():           #prio 1: turun ke anak pertama jika punya anak
            kedalaman += 1
        elif cursor.goto_next_sibling():        #prio 2: geser ke saudara sebelahnya jika tidak punya anak
            pass
        else:
            while True:                         #prio 3: naik ke induk sampai ketemu induk yang punya saudara berikutnya
                if not cursor.goto_parent():    #jika sudah mentok di atas module dan tidak bisa naik lagi, selesai
                    selesai = True
                    break
                kedalaman -= 1
                if cursor.goto_next_sibling():  #geser ke saudara induk yang belum dikunjungi
                    break

with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())               
jelajah_cursor(tree)                            