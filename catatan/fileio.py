"""Modul fileio: semua operasi baca/tulis/tambah file.

Semua operasi file memakai 'with open()' dan menyebut encoding secara
eksplisit supaya aman dijalankan di Windows maupun Linux/Mac.
"""
import os

from .processing import Pengeluaran
from .validasi import ValidasiError, validasi_baris

ENCODING = "utf-8"


def format_baris(tanggal, kategori, deskripsi, jumlah, catatan=""):
    """Rangkai satu baris file dari input. Tanda ';' di teks diganti ','
    supaya tidak merusak pemisah kolom."""
    bagian = [tanggal, kategori, deskripsi, str(jumlah)]
    if catatan:
        bagian.append(catatan)
    return ";".join(b.strip().replace(";", ",") for b in bagian)


def buat_file_data(path):
    """Buat file data baru dengan mode 'x' (eksklusif).

    Alasan 'x': aman, tidak akan menimpa data lama.
    Return True kalau berhasil dibuat, False kalau file sudah ada.
    """
    try:
        with open(path, "x", encoding=ENCODING):
            pass   # cukup dibuat kosong
        return True
    except FileExistsError:
        return False


def tambah_data(path, baris):
    """Tambah satu baris di akhir file dengan mode 'a' (append).

    Alasan 'a': data lama tetap utuh. Mode 'a' sebenarnya otomatis membuat
    file kalau belum ada, jadi keberadaan file dicek dulu supaya alur
    'buat file dulu' tetap konsisten.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File '{os.path.basename(path)}' belum ada. Buat dulu lewat menu 1."
        )
    with open(path, "a", encoding=ENCODING) as file:
        file.write(baris + "\n")


def baca_data(path):
    """Baca file data baris demi baris dengan mode 'r' (iteratif).

    Return (daftar_pengeluaran, baris_rusak).
    Baris rusak DILEWATI (tidak menghentikan program) dan dicatat sebagai
    tuple (nomor_baris, isi_baris, alasan).
    FileNotFoundError dibiarkan naik ke pemanggil agar pesannya
    ditangani di main.py.
    """
    daftar = []
    rusak = []
    with open(path, "r", encoding=ENCODING) as file:
        for nomor, baris in enumerate(file, start=1):
            if not baris.strip():
                continue   # lewati baris kosong
            try:
                data = validasi_baris(baris)
                daftar.append(Pengeluaran(**data))   
            except ValidasiError as error:
                rusak.append((nomor, baris.strip(), str(error)))
    return daftar, rusak


def tulis_laporan(path, teks):
    """Tulis laporan dengan mode 'w'.

    Alasan 'w': laporan selalu dibuat ulang dari data terbaru, jadi
    isi laporan lama memang harus ditimpa.
    """
    with open(path, "w", encoding=ENCODING) as file:
        file.write(teks + "\n")


def baca_isi(path):
    """Baca seluruh isi file (untuk menampilkan laporan di layar)."""
    with open(path, "r", encoding=ENCODING) as file:
        return file.read()
