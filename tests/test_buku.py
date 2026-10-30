# Meuthia Sari Rusdy_F5212510027
from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memastikan fungsi berhasil
    assert hasil is True

    # Memastikan execute dipanggil
    mock_cursor.execute.assert_called_once()

    # Memastikan commit dipanggil
    model.conn.commit.assert_called_once()


def test_get_all_buku():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Menyiapkan data buku tiruan
    data_buku = [
        {
            "id_buku": 1,
            "judul": "Buku Testing",
            "penulis": "Penulis QA",
            "tahun_terbit": 2026
        }
    ]

    # Mengatur hasil fetchall()
    mock_cursor.fetchall.return_value = data_buku

    # Melakukan eksekusi fungsi
    hasil = model.get_all_buku()

    # Memastikan hasil sesuai dengan data tiruan
    assert hasil == data_buku

    # Memastikan query SELECT dijalankan
    mock_cursor.execute.assert_called_once()

    # Memastikan fetchall dipanggil
    mock_cursor.fetchall.assert_called_once()

    # Memastikan cursor ditutup
    mock_cursor.close.assert_called_once()
