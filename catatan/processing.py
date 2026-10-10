"""Modul processing: class data, perhitungan, dan analisis pengeluaran.

Modul ini juga berdiri sendiri, bisa dites langsung:
python catatan/processing.py
"""
from datetime import datetime

BATAS_HARIAN_DEFAULT = 100000  


def hitung_total(*jumlah):
    """Jumlahkan sebanyak apa pun angka yang dikirim (*args -> tuple)."""
    return sum(jumlah)


def format_rupiah(angka):
    """Format angka jadi 'Rp 1.234.567'."""
    return "Rp " + f"{int(round(angka)):,}".replace(",", ".")


class Pengeluaran:
    """Satu catatan pengeluaran."""

    def __init__(self, tanggal, kategori, deskripsi, jumlah, **atribut_tambahan):
        assert isinstance(jumlah, int) and jumlah >= 0, \
            "jumlah harus bilangan bulat >= 0"
        self.tanggal = tanggal
        self.kategori = kategori
        self.deskripsi = deskripsi
        self.jumlah = jumlah
        self.atribut_tambahan = atribut_tambahan

    def __str__(self):
        teks = (f"{self.tanggal} | {self.kategori:<10} | "
                f"{self.deskripsi:<22} | {format_rupiah(self.jumlah)}")
        if self.atribut_tambahan:
            tambahan = ", ".join(f"{k}={v}" for k, v in self.atribut_tambahan.items())
            teks += f" ({tambahan})"
        return teks


class AnalisisPengeluaran:
    """Mengolah dan menganalisis kumpulan Pengeluaran."""

    def __init__(self, daftar, batas_harian=BATAS_HARIAN_DEFAULT):
        assert batas_harian > 0, "batas_harian harus lebih dari 0"
        self.daftar = daftar
        self.batas_harian = batas_harian

    def total(self):
        """Total seluruh pengeluaran. map + lambda mengambil kolom jumlah,
        lalu di-unpack ke *args milik hitung_total."""
        return hitung_total(*map(lambda p: p.jumlah, self.daftar))

    def total_per_tanggal(self):
        """Dict {tanggal: total pengeluaran hari itu}."""
        hasil = {}
        for p in self.daftar:
            hasil[p.tanggal] = hasil.get(p.tanggal, 0) + p.jumlah
        return hasil

    def total_per_kategori(self):
        """Dict {kategori: total pengeluaran kategori itu}."""
        hasil = {}
        for p in self.daftar:
            hasil[p.kategori] = hasil.get(p.kategori, 0) + p.jumlah
        return hasil

    def rata_rata_harian(self):
        """Rata-rata pengeluaran per hari yang tercatat (0 kalau data kosong)."""
        per_hari = self.total_per_tanggal()
        if not per_hari:
            return 0
        return self.total() / len(per_hari)

    def terbesar(self):
        """Pengeluaran dengan jumlah paling besar (None kalau data kosong)."""
        if not self.daftar:
            return None
        return max(self.daftar, key=lambda p: p.jumlah)

    def hari_boros(self):
        """Daftar tanggal yang total pengeluarannya melebihi batas_harian."""
        return sorted(t for t, tot in self.total_per_tanggal().items()
                      if tot > self.batas_harian)

    def urutkan(self, berdasarkan="jumlah", terbalik=True):
        """Urutkan daftar berdasarkan atribut tertentu (lambda sebagai key)."""
        return sorted(self.daftar,
                      key=lambda p: getattr(p, berdasarkan),
                      reverse=terbalik)

    def filter_kategori(self, kategori):
        """Ambil hanya pengeluaran dari satu kategori (filter + lambda)."""
        return list(filter(lambda p: p.kategori == kategori.lower(), self.daftar))


def buat_laporan(analisis, jumlah_rusak=0):
    """Susun teks laporan lengkap dari objek AnalisisPengeluaran."""
    garis = "=" * 56
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
    baris = [
        garis,
        "LAPORAN PENGELUARAN HARIAN",
        f"Dibuat pada       : {waktu}",
        garis,
        f"Jumlah transaksi  : {len(analisis.daftar)}",
        f"Total pengeluaran : {format_rupiah(analisis.total())}",
        f"Rata-rata per hari: {format_rupiah(analisis.rata_rata_harian())}",
    ]

    besar = analisis.terbesar()
    if besar is not None:
        baris.append(f"Terbesar          : {besar.deskripsi} "
                     f"({format_rupiah(besar.jumlah)}) pada {besar.tanggal}")

    baris.append("")
    baris.append("Total per kategori:")
    for kategori, total in sorted(analisis.total_per_kategori().items(),
                                  key=lambda kv: kv[1], reverse=True):
        baris.append(f"  - {kategori:<10}: {format_rupiah(total)}")

    boros = analisis.hari_boros()
    baris.append("")
    baris.append(f"Hari boros (> {format_rupiah(analisis.batas_harian)}): "
                 f"{', '.join(boros) if boros else 'tidak ada'}")

    baris.append("")
    baris.append("Daftar transaksi (dari terbesar):")
    for p in analisis.urutkan(berdasarkan="jumlah", terbalik=True):
        baris.append(f"  {p}")

    if jumlah_rusak:
        baris.append("")
        baris.append(f"Catatan: {jumlah_rusak} baris data rusak dilewati.")
    baris.append(garis)
    return "\n".join(baris)


if __name__ == "__main__":
    contoh = [
        Pengeluaran("2026-10-05", "makanan", "Makan siang", 25000),
        Pengeluaran("2026-10-06", "hiburan", "Nonton bioskop", 120000,
                    catatan="bareng teman"),
    ]
    print(buat_laporan(AnalisisPengeluaran(contoh, batas_harian=100000)))
