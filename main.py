"""Program utama: Pencatatan Pengeluaran Harian.

Jalankan dari folder pencatatan_harian:
    python main.py
"""
import os
import unittest
from datetime import date

from catatan import (AnalisisPengeluaran, ValidasiError, baca_data, baca_isi, buat_file_data, buat_laporan, format_baris, tambah_data, tulis_laporan, validasi_baris)

FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_DATA = os.path.join(FOLDER, "data_pengeluaran.txt")
FILE_LAPORAN = os.path.join(FOLDER, "laporan_pengeluaran.txt")


def tampilkan_menu():
    print("\n===== PENCATATAN PENGELUARAN HARIAN =====")
    print("1. Buat file data baru")
    print("2. Tambah pengeluaran")
    print("3. Tampilkan semua data")
    print("4. Analisis & buat laporan")
    print("5. Jalankan pengujian (unittest)")
    print("6. Keluar")


def menu_buat_file():
    if buat_file_data(FILE_DATA):
        print("File data berhasil dibuat.")
    else:
        print("Gagal: file data sudah ada, data lama tidak ditimpa.")


def menu_tambah():
    hari_ini = date.today().isoformat()
    tanggal = input(f"Tanggal (YYYY-MM-DD, Enter = {hari_ini}): ").strip() or hari_ini
    kategori = input("Kategori (mis. makanan/transport): ")
    deskripsi = input("Deskripsi: ")
    jumlah = input("Jumlah (Rp, angka bulat): ")
    catatan = input("Catatan (opsional, Enter untuk lewati): ")

    baris = format_baris(tanggal=tanggal, kategori=kategori, deskripsi=deskripsi,
                         jumlah=jumlah, catatan=catatan)
    try:
        validasi_baris(baris)        
        tambah_data(FILE_DATA, baris)
        print("Data berhasil ditambahkan.")
    except ValidasiError as error:
        print(f"Input tidak valid: {error}")
    except FileNotFoundError as error:
        print(f"Error: {error}")


def menu_tampilkan():
    try:
        daftar, rusak = baca_data(FILE_DATA)
    except FileNotFoundError:
        print("Error: file data_pengeluaran.txt belum ada. Pilih menu 1 dulu.")
        return

    if not daftar:
        print("Belum ada data yang valid.")
    for nomor, pengeluaran in enumerate(daftar, start=1):
        print(f"{nomor}. {pengeluaran}")
    tampilkan_baris_rusak(rusak)


def tampilkan_baris_rusak(rusak):
    """Tampilkan baris rusak yang dilewati (kalau ada)."""
    if rusak:
        print(f"\n{len(rusak)} baris rusak dilewati:")
        for nomor, isi, alasan in rusak:
            print(f"  baris {nomor}: {isi}  ->  {alasan}")


def menu_analisis():
    try:
        daftar, rusak = baca_data(FILE_DATA)
    except FileNotFoundError:
        print("Error: file data_pengeluaran.txt belum ada. Pilih menu 1 dulu.")
        return

    if not daftar:
        print("Belum ada data valid untuk dianalisis.")
        return

    analisis = AnalisisPengeluaran(daftar, batas_harian=100000)
    laporan = buat_laporan(analisis, jumlah_rusak=len(rusak))
    tulis_laporan(FILE_LAPORAN, laporan)      
    print(baca_isi(FILE_LAPORAN))             
    print(f"Laporan juga disimpan di: {FILE_LAPORAN}")


def menu_pengujian():
    from catatan import testing
    suite = unittest.defaultTestLoader.loadTestsFromModule(testing)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main():
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-6): ").strip()
        if pilihan == "1":
            menu_buat_file()
        elif pilihan == "2":
            menu_tambah()
        elif pilihan == "3":
            menu_tampilkan()
        elif pilihan == "4":
            menu_analisis()
        elif pilihan == "5":
            menu_pengujian()
        elif pilihan == "6":
            print("Terima kasih, sampai jumpa!")
            break
        else:
            print("Pilihan tidak dikenali, coba lagi.")


if __name__ == "__main__":
    main()
