import customtkinter as ctk
from tkinter import ttk

class AnggotaView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("800x450")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # FRAME KIRI: FORM INPUT ANGGOTA
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Anggota", font=("Arial", 16, "bold")).pack(pady=15)

        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Anggota")
        self.entry_nama.pack(pady=10, padx=15, fill="x")

        self.entry_alamat = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Alamat")
        self.entry_alamat.pack(pady=10, padx=15, fill="x")

        self.btn_simpan = ctk.CTkButton(self.frame_kiri,text="Simpan Data",fg_color="green")
        self.btn_simpan.pack(pady=15, padx=15, fill="x")

        # FRAME KANAN: TABEL DAFTAR ANGGOTA
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Anggota", font=("Arial", 16, "bold")).pack(pady=15)

        kolom = ("id_anggota", "nama", "alamat")
        self.table = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        self.table.heading("id_anggota", text="ID")
        self.table.heading("nama", text="Nama Anggota")
        self.table.heading("alamat", text="Alamat")

        self.table.column("id_anggota", width=50, anchor="center")
        self.table.column("nama", width=150)
        self.table.column("alamat", width=200)

        self.table.pack(fill="both", expand=True, padx=15, pady=10)

if __name__ == "__main__":
    app = AnggotaView()
    app.mainloop()