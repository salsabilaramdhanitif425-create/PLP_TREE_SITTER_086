def hitung_diskon(harga, persen):
    potongan = harga * persen / 100  #menghitung nominal potongan dari persentase
    return harga - potongan          #mengembalikan harga akhir setelah dikurangi potongan