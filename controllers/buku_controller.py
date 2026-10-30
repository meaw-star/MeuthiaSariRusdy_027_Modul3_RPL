# Meuthia Sari Rusdy_F5212510027
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        # Binding tombol simpan, update, delete, dan logout
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.btn_logout.configure(command=self.logout)

        # Binding pemilihan baris tabel
        self.view.table.bind("<<TreeviewSelect>>", self.pilih_buku)

        # TUGAS MEUTHIA MODUL 7 NOMOR 2: Menerapkan aturan otorisasi pada tombol Update dan Delete
        # Jika pengguna bukan admin, tombol dan form akan dikunci
        if self.user_role != "admin":
            self.view.btn_simpan.configure(
                state="disabled",
                text="Akses Terkunci (Khusus Admin)"
            )
            self.view.btn_update.configure(state="disabled")
            self.view.btn_delete.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        # Mengosongkan isi tabel di View terlebih dahulu
        for item in self.view.table.get_children():
            self.view.table.delete(item)

        # Mengambil data dari Model (database)
        data_buku = self.model.get_all_buku()

        # Memasukkan data baru ke dalam tabel View
        for buku in data_buku:
            self.view.table.insert(
                "", "end",
                values=(
                    buku['id_buku'],
                    buku['judul'],
                    buku['penulis'],
                    buku['tahun_terbit']
                )
            )

    def simpan_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menambah data!"
            )
            return

        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        # Validasi Form Kosong
        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil disimpan!"
            )

            # Bersihkan form input
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')

            # Muat ulang tabel
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Gagal menyimpan data."
            )

    # Memilih buku dari tabel
    def pilih_buku(self, event=None):
        if self.user_role != "admin":
            return

        pilihan = self.view.table.selection()

        if not pilihan:
            return

        data = self.view.table.item(pilihan[0], "values")

        self.view.entry_judul.delete(0, 'end')
        self.view.entry_judul.insert(0, data[1])

        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_penulis.insert(0, data[2])

        self.view.entry_tahun.delete(0, 'end')
        self.view.entry_tahun.insert(0, data[3])

    # Memperbarui data buku
    def update_data(self):
        # Proteksi hak akses
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk memperbarui data!"
            )
            return

        pilihan = self.view.table.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin diperbarui!"
            )
            return

        data = self.view.table.item(pilihan[0], "values")
        id_buku = data[0]

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi!"
            )
            return

        berhasil = self.model.update_buku(
            id_buku, judul, penulis, tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil diperbarui!"
            )

            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')

            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat memperbarui data."
            )

    # Menghapus data buku
    def hapus_data(self):
        # Proteksi hak akses
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menghapus data!"
            )
            return

        pilihan = self.view.table.selection()

        if not pilihan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih buku yang ingin dihapus!"
            )
            return

        data = self.view.table.item(pilihan[0], "values")
        id_buku = data[0]
        judul = data[1]

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus buku '{judul}'?"
        )

        if not konfirmasi:
            return

        berhasil = self.model.delete_buku(id_buku)

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil dihapus!"
            )

            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')

            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Terjadi kesalahan saat menghapus data."
            )

    # TUGAS MEUTHIA MODUL 7 NOMOR 3:
    # Fungsi Logout untuk kembali ke halaman Login
    def logout(self):
        # Menutup jendela perpustakaan
        self.view.destroy()

        # Membuka kembali halaman Login
        from controllers.auth_controller import AuthController
        app_auth = AuthController()
        app_auth.run()

    # Fungsi untuk menyalakan aplikasi
    def run(self):
        self.view.mainloop()
