; 1. Menangkap nama modul pada 'import os' (atau 'import os.path')
(import_statement
  name: (dotted_name) @modul)

; 2. Menangkap nama modul asli pada 'import sys as sistem' (mengabaikan alias)
(import_statement
  name: (aliased_import
    name: (dotted_name) @modul))

; 3. Menangkap nama modul asal pada 'from pathlib import Path' dan 'from math import sqrt, pi'
(import_from_statement
  module_name: (dotted_name) @modul)