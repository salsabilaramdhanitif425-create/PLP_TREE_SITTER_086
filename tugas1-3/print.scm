(call
  function: (identifier) @_fn   ; menangkap nama fungsi ke variabel bantu @_fn (diawali _ agar tidak ikut dicetak)
  (#eq? @_fn "print")) @print_call ; menyaring hanya jika nama fungsinya "print", lalu menangkap seluruh node call sebagai @print_call