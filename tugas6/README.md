# Pendeteksi TODO, Fungsi Panjang, dan Error Sintaks (`cek.py`)

CLI berbasis **Tree-sitter** untuk menganalisis file **Python (`.py`)** dan **JavaScript (`.js`)** secara statis.

## Fitur

1. **Deteksi Komentar `TODO` / `FIXME`:** Menemukan komentar yang memuat `TODO` atau `FIXME` menggunakan query Tree-sitter dan predikat `#match?`.
2. **Deteksi Fungsi Panjang:** Melaporkan fungsi dengan panjang lebih dari **30 baris** (`end_point[0] - start_point[0] + 1 > 30`). *Catatan: seluruh definisi fungsi, termasuk method di dalam kelas dan fungsi bersarang, ikut dihitung.*
3. **Deteksi Error Sintaks:** Memeriksa `root_node.has_error` dan menelusuri pohon parse secara rekursif untuk melaporkan baris pertama yang bermasalah.
4. **Dukungan JavaScript (Pengayaan):** Mendukung pemindaian file `.js` menggunakan `tree-sitter-javascript`, serta otomatis melewati direktori `venv/`, `.venv/`, `.git/`, `__pycache__/`, dan `node_modules/`.

## Instalasi Dependensi

```bash
pip install tree-sitter tree-sitter-python tree-sitter-javascript