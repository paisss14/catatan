"""Modul validasi: mengecek input dan baris data pengeluaran.

Modul ini berdiri sendiri (tidak mengimpor modul lain di package),
jadi bisa dites langsung: python catatan/validasi.py
"""
from datetime import datetime

FORMAT_TANGGAL = "%Y-%m-%d"   
PEMISAH = ";"                 

class ValidasiError(ValueError):
    """Exception buatan sendiri untuk data yang tidak valid."""

def parse_jumlah(teks):
    """Ubah teks jadi angka bulat >= 0.

    - try/except menangkap ValueError saat konversi gagal.
    - raise memunculkan ValidasiError untuk nilai negatif.
    """
    try:
        jumlah = int(str(teks).strip())
    except ValueError:
        raise ValidasiError(f"Jumlah '{teks}' bukan angka bulat") from None

    if jumlah < 0:
        raise ValidasiError(f"Jumlah tidak boleh negatif (diterima: {jumlah})")
    return jumlah

def validasi_tanggal(teks):
    """Pastikan tanggal berformat YYYY-MM-DD dan benar-benar ada di kalender."""
    try:
        datetime.strptime(teks.strip(), FORMAT_TANGGAL)
    except ValueError:
        raise ValidasiError(
            f"Tanggal '{teks}' tidak valid (format harus YYYY-MM-DD)"
        ) from None
    return teks.strip()

def cek_field_kosong(**field):
    """Cek banyak field sekaligus. **field = pasangan nama=nilai.

    Contoh: cek_field_kosong(kategori="makanan", deskripsi="")
    -> raise ValidasiError karena deskripsi kosong.
    """
    for nama, nilai in field.items():
        if not str(nilai).strip():
            raise ValidasiError(f"Field '{nama}' tidak boleh kosong")

def validasi_baris(baris):
    """Pecah satu baris file jadi dict yang sudah tervalidasi.

    Format baris: tanggal;kategori;deskripsi;jumlah[;catatan]
    Kolom catatan bersifat opsional.
    """
    bagian = [b.strip() for b in baris.strip().split(PEMISAH)]

    if len(bagian) not in (4, 5):
        raise ValidasiError(
            f"Jumlah kolom salah: {len(bagian)} (seharusnya 4 atau 5)"
        )

    tanggal, kategori, deskripsi, jumlah = bagian[:4]
    cek_field_kosong(tanggal=tanggal, kategori=kategori,
                     deskripsi=deskripsi, jumlah=jumlah)

    data = {
        "tanggal": validasi_tanggal(tanggal),
        "kategori": kategori.lower(),     
        "deskripsi": deskripsi,
        "jumlah": parse_jumlah(jumlah),
    }
    if len(bagian) == 5 and bagian[4]:
        data["catatan"] = bagian[4]
    return data

if __name__ == "__main__":
    print(validasi_baris("2026-10-10;Makanan;Nasi goreng;15000"))
    try:
        validasi_baris("2026-10-10;makanan;Nasi goreng;abc")
    except ValidasiError as e:
        print("Error tertangkap:", e)
