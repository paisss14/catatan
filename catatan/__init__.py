"""Package catatan: program pencatatan pengeluaran harian.

File ini dieksekusi saat package di-import. Di sini function/class penting
di-export supaya main.py bisa memanggilnya langsung dari 'catatan'.
"""
from .validasi import ValidasiError, validasi_baris, parse_jumlah
from .processing import (Pengeluaran, AnalisisPengeluaran, buat_laporan, hitung_total, format_rupiah)
from .fileio import (buat_file_data, tambah_data, baca_data,tulis_laporan, baca_isi, format_baris)
