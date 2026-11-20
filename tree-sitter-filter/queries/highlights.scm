; Nama kolom / field
(identifier) @property

; Literal nilai
(string) @string
(number) @number
(boolean) @constant.builtin

; Kata kunci logika & operator khusus Tugas 4
[
  "and"
  "or"
  "not"
  "in"
  "contains"
] @keyword

; Operator perbandingan
[
  "="
  "!="
  ">"
  "<"
  ">="
  "<="
] @operator

; Tanda baca pengelompokan & pemisah daftar
[
  "("
  ")"
  "["
  "]"
] @punctuation.bracket

"," @punctuation.delimiter