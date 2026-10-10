"""Modul testing: unit test memakai library unittest.

Cara menjalankan (dari folder pencatatan_harian):
    python -m catatan.testing
atau lewat menu 5 di main.py
"""
import os
import tempfile
import unittest

from ..fileio import baca_data, buat_file_data, tambah_data, tulis_laporan, baca_isi
from .processing import AnalisisPengeluaran, Pengeluaran
from .validasi import (ValidasiError, cek_field_kosong, parse_jumlah,
                       validasi_baris, validasi_tanggal)


class TestValidasi(unittest.TestCase):
    """Pengujian modul validasi."""

    def test_parse_jumlah_valid(self):
        self.assertEqual(parse_jumlah("15000"), 15000)

    def test_parse_jumlah_negatif(self):
        with self.assertRaises(ValidasiError):
            parse_jumlah("-500")

    def test_parse_jumlah_bukan_angka(self):
        with self.assertRaises(ValidasiError):
            parse_jumlah("abc")

    def test_tanggal_tidak_valid(self):
        with self.assertRaises(ValidasiError):
            validasi_tanggal("2026-13-45")

    def test_field_kosong(self):
        with self.assertRaises(ValidasiError):
            cek_field_kosong(kategori="makanan", deskripsi="  ")

    def test_baris_valid_dengan_catatan(self):
        data = validasi_baris("2026-10-05;Makanan;Bakso;20000;enak")
        self.assertEqual(data["kategori"], "makanan")   # otomatis huruf kecil
        self.assertEqual(data["catatan"], "enak")


class TestAnalisis(unittest.TestCase):
    """Pengujian class AnalisisPengeluaran."""

    def setUp(self):
        self.analisis = AnalisisPengeluaran([
            Pengeluaran("2026-10-05", "makanan", "Makan siang", 25000),
            Pengeluaran("2026-10-05", "transport", "Ojek", 15000),
            Pengeluaran("2026-10-06", "makanan", "Makan malam", 30000),
            Pengeluaran("2026-10-06", "hiburan", "Nonton", 120000),
        ], batas_harian=100000)

    def test_total(self):
        self.assertEqual(self.analisis.total(), 190000)

    def test_total_per_kategori(self):
        self.assertEqual(self.analisis.total_per_kategori(),
                         {"makanan": 55000, "transport": 15000, "hiburan": 120000})

    def test_rata_rata_harian(self):
        self.assertEqual(self.analisis.rata_rata_harian(), 95000)

    def test_hari_boros(self):
        self.assertEqual(self.analisis.hari_boros(), ["2026-10-06"])

    def test_urutkan_terbesar_dulu(self):
        self.assertEqual(self.analisis.urutkan()[0].deskripsi, "Nonton")

    def test_filter_kategori(self):
        hasil = self.analisis.filter_kategori("MAKANAN")
        self.assertEqual(len(hasil), 2)

    def test_data_kosong_tidak_error(self):
        kosong = AnalisisPengeluaran([])
        self.assertEqual(kosong.total(), 0)
        self.assertEqual(kosong.rata_rata_harian(), 0)
        self.assertIsNone(kosong.terbesar())


class TestFileIO(unittest.TestCase):
    """Pengujian modul fileio memakai folder sementara (data asli aman)."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)  
        self.path = os.path.join(folder.name, "data.txt")

    def test_buat_file_dua_kali(self):
        self.assertTrue(buat_file_data(self.path))    
        self.assertFalse(buat_file_data(self.path))   

    def test_tambah_tanpa_file(self):
        with self.assertRaises(FileNotFoundError):
            tambah_data(self.path, "2026-10-05;makanan;Bakso;20000")

    def test_baca_lewati_baris_rusak(self):
        buat_file_data(self.path)
        tambah_data(self.path, "2026-10-05;makanan;Bakso;20000")
        tambah_data(self.path, "2026-10-05;makanan;Rusak;abc")
        tambah_data(self.path, "2026-10-06;transport;Ojek;15000")
        daftar, rusak = baca_data(self.path)
        self.assertEqual(len(daftar), 2)
        self.assertEqual(len(rusak), 1)
        self.assertEqual(rusak[0][0], 2)   

    def test_baca_file_tidak_ada(self):
        with self.assertRaises(FileNotFoundError):
            baca_data(self.path)

    def test_tulis_laporan_menimpa(self):
        tulis_laporan(self.path, "isi lama")
        tulis_laporan(self.path, "isi baru")
        self.assertEqual(baca_isi(self.path).strip(), "isi baru")


if __name__ == "__main__":
    unittest.main()
