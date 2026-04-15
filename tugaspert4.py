import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# 1. Bagian Brain Center (Basis Pengetahuan)
# Data kerusakan hardware komputer
db_kerusakan = {
    "Gangguan RAM (Memori)": {
        "ciri": ["bunyi_beep", "restart_sendiri", "blue_screen"],
        "penanganan": "Lepaskan RAM, bersihkan bagian pin emas dengan penghapus secara perlahan. Pasang kembali atau pindahkan ke slot lain. Jika masih error, kemungkinan RAM perlu diganti."
    },
    "Masalah Power Supply Unit": {
        "ciri": ["mati_mendadak", "bau_gosong", "kipas_tidak_mutar"],
        "penanganan": "Cek kabel power dan stabilitas listrik. Jika tercium aroma hangus atau kipas mati, segera ganti PSU sebelum merusak komponen Motherboard lainnya."
    },
    "Overheating System": {
        "ciri": ["kinerja_lambat", "mati_saat_berat", "kipas_berisik"],
        "penanganan": "Bersihkan debu pada heatsink dan fan. Pastikan pasta termal (thermal paste) pada prosesor masih layak atau ganti dengan yang baru untuk suhu lebih optimal."
    },
    "Kerusakan Unit Grafis (VGA)": {
        "ciri": ["layar_bergaris", "layar_blank", "game_crash"],
        "penanganan": "Update driver ke versi terbaru. Bersihkan konektor VGA. Jika muncul artefak (garis permanen), biasanya ada masalah pada chipset GPU."
    },
    "Storage Error (HDD/SSD)": {
        "ciri": ["booting_lama", "file_corrupt", "bunyi_klik"],
        "penanganan": "Segera lakukan backup data ke cloud atau eksternal. Gunakan software pengecek kesehatan disk. Ganti ke SSD jika performa sudah menurun drastis."
    }
}

indeks_gejala = {
    "bunyi_beep": "PC mengeluarkan suara beep berulang",
    "restart_sendiri": "Sering melakukan restart otomatis",
    "blue_screen": "Muncul layar biru (BSOD) secara acak",
    "mati_mendadak": "Unit mati total secara tiba-tiba",
    "bau_gosong": "Ada aroma terbakar dari dalam unit",
    "kipas_tidak_mutar": "Kipas pada PSU tidak bergerak",
    "kinerja_lambat": "Sistem terasa sangat lemot/lagging",
    "mati_saat_berat": "Mati saat membuka game atau render video",
    "kipas_berisik": "Suara kipas terdengar sangat kencang",
    "layar_bergaris": "Ada gangguan visual (garis/kotak) di monitor",
    "layar_blank": "Mesin menyala tapi tidak ada gambar",
    "game_crash": "Aplikasi/Game tertutup sendiri (Force Close)",
    "booting_lama": "Loading masuk sistem operasi sangat lambat",
    "file_corrupt": "Data sering hilang atau tidak bisa dibuka",
    "bunyi_klik": "Ada suara ketukan mekanik dari arah penyimpanan"
}

def analisa_kerusakan(list_gejala):
    temuan = []
    
    if not list_gejala:
        return temuan
        
    for nama_error, info in db_kerusakan.items():
        syarat_error = set(info["ciri"])
        pilihan_user = set(list_gejala)
        
        # Mencari kecocokan gejala
        match_count = len(syarat_error.intersection(pilihan_user))
        
        if match_count >= 2:
            temuan.append({
                "kategori": nama_error,
                "tindakan": info["penanganan"]
            })
            
    return temuan


# 2. Antarmuka Pengguna (GUI)

class PakarHardwareApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expert System: Diagnostic Hardware v1.0")
        self.master.geometry("600x750")
        self.master.configure(bg="#f0f2f5")
        
        # Header
        self.lbl_judul = tk.Label(master, text="🔍 Hardware Diagnostic Center", font=("Segoe UI", 15, "bold"), bg="#f0f2f5", fg="#2c3e50")
        self.lbl_judul.pack(pady=15)
        
        self.lbl_info = tk.Label(master, text="Pilih gejala yang dialami oleh komputer Anda:", font=("Segoe UI", 9), bg="#f0f2f5")
        self.lbl_info.pack(pady=2)
        
        # Container Checkbox
        self.box_container = tk.Frame(master, bg="#ffffff", highlightbackground="#d1d4d7", highlightthickness=1)
        self.box_container.pack(pady=10, padx=25, fill="both", expand=True)

        self.input_status = {}
        
        # Generate Checkbox secara dinamis
        for key, val in indeks_gejala.items():
            status_var = tk.BooleanVar()
            check_btn = tk.Checkbutton(self.box_container, text=val, variable=status_var, bg="#ffffff", font=("Segoe UI", 9), anchor="w")
            check_btn.pack(fill="x", padx=15, pady=3)
            self.input_status[key] = status_var

        # Action Button
        self.btn_cek = tk.Button(master, text="Mulai Diagnosa", font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white", activebackground="#2980b9", relief="flat", command=self.eksekusi_logika)
        self.btn_cek.pack(pady=20, ipadx=20, ipady=8)
        
        # Output Area
        self.group_output = tk.LabelFrame(master, text=" Ringkasan Analisis ", font=("Segoe UI", 9, "bold"), bg="#f0f2f5")
        self.group_output.pack(pady=10, padx=25, fill="both", expand=True)
        
        self.viewer_teks = tk.Text(self.group_output, height=8, bg="#ffffff", font=("Courier New", 10), wrap="word", state="disabled", borderwidth=0)
        self.viewer_teks.pack(padx=10, pady=10, fill="both", expand=True)

    def eksekusi_logika(self):
        # Ambil list gejala yang dicentang
        pilihan = [k for k, v in self.input_status.items() if v.get()]
        
        # Panggil fungsi mesin inferensi
        data_hasil = analisa_kerusakan(pilihan)
        
        self.viewer_teks.config(state="normal")
        self.viewer_teks.delete(1.0, tk.END)
        
        if len(pilihan) < 1:
            messagebox.showwarning("Input Kosong", "Silakan pilih setidaknya satu gejala terlebih dahulu.")
            self.viewer_teks.insert(tk.END, "Status: Menunggu input...")
        
        elif not data_hasil:
            self.viewer_teks.insert(tk.END, "HASIL TIDAK DITEMUKAN\n" + "-"*30)
            self.viewer_teks.insert(tk.END, "\nGejala yang Anda pilih tidak menunjukkan pola kerusakan spesifik pada basis data kami. Disarankan melakukan pengecekan fisik menyeluruh.")
            
        else:
            self.viewer_teks.insert(tk.END, "LAPORAN DIAGNOSA HARDWARE\n")
            self.viewer_teks.insert(tk.END, "="*40 + "\n\n")
            
            for i, poin in enumerate(data_hasil):
                self.viewer_teks.insert(tk.END, f"[{i+1}] KERUSAKAN: {poin['kategori']}\n")
                self.viewer_teks.insert(tk.END, f"    SOLUSI  : {poin['tindakan']}\n\n")
                
        self.viewer_teks.config(state="disabled")

# Main Execution
if __name__ == "__main__":
    app_root = tk.Tk()
    run_app = PakarHardwareApp(app_root)
    app_root.mainloop()