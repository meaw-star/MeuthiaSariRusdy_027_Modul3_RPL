# Tugas Modul 7 Meuthia Sari Rusdy_F5212510027
import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView


class AnggotaController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = AnggotaModel()
        self.view = AnggotaView()

        # Menghubungkan tombol Simpan dengan fungsi simpan_data
        self.view.btn_simpan.configure(command=self.simpan_data)

        # Memuat data anggota ke tabel
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan tabel terlebih dahulu
        for item in self.view.table.get_children():
            self.view.table.delete(item)

        # Mengambil data anggota dari Model
        data_anggota = self.model.get_all_anggota()

        # Menampilkan data anggota ke tabel
        for anggota in data_anggota:
            self.view.table.insert(
                "",
                "end",
                values=(
                    anggota["id_anggota"],
                    anggota["nama"],
                    anggota["alamat"]
                )
            )

    def simpan_data(self):
        # Mengambil data dari form
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        # Memeriksa apakah form kosong
        if not nama or not alamat:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        # Menyimpan data melalui Model
        berhasil = self.model.create_anggota(nama, alamat)

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil disimpan!"
            )

            # Mengosongkan form
            self.view.entry_nama.delete(0, "end")
            self.view.entry_alamat.delete(0, "end")

            # Memuat ulang tabel
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menyimpan data."
            )

    # Menjalankan aplikasi
    def run(self):
        self.view.mainloop()


if __name__ == "__main__":
    app = AnggotaController()
    app.run()
