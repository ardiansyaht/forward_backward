import tkinter as tk
from tkinter import ttk, messagebox

class ExpertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Pakar - Menu Utama")
        self.geometry("700x600")
        
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.homepage = HomePage(self.container, self)
        self.forward_page = ForwardChainingPage(self.container, self)
        self.backward_page = BackwardChainingPage(self.container, self)
        
        self.show_frame(self.homepage)
    
    def show_frame(self, frame):
        for widget in self.container.winfo_children():
            widget.pack_forget()
        frame.pack(fill="both", expand=True)
        self.title(f"Sistem Pakar - {frame.title}")

class HomePage(ttk.Frame):
    title = "Menu Utama"
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Pilih Metode Inferensi", font=("Arial", 20)).pack(pady=30)
        
        btn_forward = ttk.Button(self, text="Forward Chaining", width=25,
                                 command=lambda: controller.show_frame(controller.forward_page))
        btn_forward.pack(pady=15)
        
        btn_backward = ttk.Button(self, text="Backward Chaining", width=25,
                                  command=lambda: controller.show_frame(controller.backward_page))
        btn_backward.pack(pady=15)

class ForwardChainingPage(ttk.Frame):
    title = "Forward Chaining"
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Label(self, text="Forward Chaining", font=("Arial", 16)).pack(pady=10)
        
        ttk.Label(self, text="Masukkan umur:").pack()
        self.entry_umur = ttk.Entry(self)
        self.entry_umur.pack()

        self.var_member = tk.BooleanVar()
        self.chk_member = ttk.Checkbutton(self, text="Member?", variable=self.var_member)
        self.chk_member.pack()

        ttk.Label(self, text="Saldo (minimal 100):").pack()
        self.entry_saldo = ttk.Entry(self)
        self.entry_saldo.pack()

        self.var_blacklist = tk.BooleanVar()
        self.chk_blacklist = ttk.Checkbutton(self, text="Masuk daftar blacklist?", variable=self.var_blacklist)
        self.chk_blacklist.pack()

        self.var_tanggal_valid = tk.BooleanVar(value=True)
        self.chk_tanggal_valid = ttk.Checkbutton(self, text="Tanggal pembelian valid?", variable=self.var_tanggal_valid)
        self.chk_tanggal_valid.pack()

        ttk.Label(self, text="Jenis tiket:").pack()
        self.combo_jenis_tiket = ttk.Combobox(self, values=["VIP", "Reguler", "Ekonomi"])
        self.combo_jenis_tiket.pack()
        self.combo_jenis_tiket.current(0)
        
        ttk.Button(self, text="Proses", command=self.proses).pack(pady=10)

        # Frame hasil dua kolom
        self.frame_hasil = ttk.Frame(self)
        self.frame_hasil.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Label(self.frame_hasil, text="Aturan yang diterapkan:").grid(row=0, column=0, sticky="w")
        self.text_rules = tk.Text(self.frame_hasil, width=30, height=15)
        self.text_rules.grid(row=1, column=0, sticky="nsew", padx=(0,10))

        ttk.Label(self.frame_hasil, text="Kesimpulan dan Fakta:").grid(row=0, column=1, sticky="w")
        self.text_summary = tk.Text(self.frame_hasil, width=50, height=15)
        self.text_summary.grid(row=1, column=1, sticky="nsew")

        self.frame_hasil.columnconfigure(0, weight=1)
        self.frame_hasil.columnconfigure(1, weight=2)
        self.frame_hasil.rowconfigure(1, weight=1)
        
        ttk.Button(self, text="Kembali ke Menu Utama",
                   command=lambda: controller.show_frame(controller.homepage)).pack(pady=5)

    # Aturan forward chaining
    def rule4(self, facts):
        if facts.get("saldo", 0) < 100.0:
            if facts.get("bisa_beli_tiket") != False:
                facts["bisa_beli_tiket"] = False
                facts["alasan_tidak_bisa"] = "Saldo tidak cukup"
                return True
        return False

    def rule5(self, facts):
        if facts.get("blacklist", False):
            if facts.get("bisa_beli_tiket") != False:
                facts["bisa_beli_tiket"] = False
                facts["alasan_tidak_bisa"] = "Pengguna dalam daftar blacklist"
                return True
        return False

    def rule6(self, facts):
        if not facts.get("tanggal_valid", True):
            if facts.get("bisa_beli_tiket") != False:
                facts["bisa_beli_tiket"] = False
                facts["alasan_tidak_bisa"] = "Tanggal pembelian tidak valid"
                return True
        return False

    def rule7(self, facts):
        if facts.get("jenis_tiket") not in ["VIP", "Reguler", "Ekonomi"]:
            if facts.get("bisa_beli_tiket") != False:
                facts["bisa_beli_tiket"] = False
                facts["alasan_tidak_bisa"] = "Jenis tiket tidak valid"
                return True
        return False

    def rule1(self, facts):
        if facts["umur"] > 17:
            if facts.get("bisa_beli_tiket") != False and facts.get("bisa_beli_tiket") != True:
                facts["bisa_beli_tiket"] = True
                return True
        return False

    def rule2(self, facts):
        if facts.get("member", False):
            if "diskon" not in facts:
                facts["diskon"] = 0.1
                return True
        return False

    def forward_chaining(self, facts):
        applied_rules = []
        rules = [self.rule5, self.rule6, self.rule7, self.rule4, self.rule1, self.rule2]
        rule_applied = True
        iteration = 0
        while rule_applied:
            iteration += 1
            if iteration > 50:
                print("Warning: Loop forward chaining dihentikan karena terlalu banyak iterasi")
                break
            rule_applied = False
            for rule in rules:
                if rule(facts):
                    print(f"Rule diterapkan: {rule.__name__}")
                    applied_rules.append(rule.__name__)
                    rule_applied = True
            if not rule_applied:
                break
        return applied_rules, facts

    def proses(self):
        self.text_rules.delete("1.0", tk.END)
        self.text_summary.delete("1.0", tk.END)
        try:
            umur = int(self.entry_umur.get())
        except ValueError:
            messagebox.showerror("Error", "Umur harus berupa angka")
            return
        member = self.var_member.get()
        try:
            saldo = float(self.entry_saldo.get())
        except ValueError:
            messagebox.showerror("Error", "Saldo harus berupa angka")
            return
        blacklist = self.var_blacklist.get()
        tanggal_valid = self.var_tanggal_valid.get()
        jenis_tiket = self.combo_jenis_tiket.get()

        facts = {
            "umur": umur,
            "member": member,
            "saldo": saldo,
            "blacklist": blacklist,
            "tanggal_valid": tanggal_valid,
            "jenis_tiket": jenis_tiket
        }

        applied_rules, updated_facts = self.forward_chaining(facts)

        for rule in applied_rules:
            self.text_rules.insert(tk.END, f"- {rule}\n")

        hasil = ""
        if updated_facts.get("bisa_beli_tiket") == False:
            hasil += f"Tidak bisa membeli tiket karena: {updated_facts.get('alasan_tidak_bisa', 'Alasan tidak diketahui')}\n"
        elif updated_facts.get("bisa_beli_tiket"):
            hasil += "Kesimpulan: Anda bisa membeli tiket!\n"
            posisi_duduk = {
                "VIP": "Duduk di area VIP, dekat panggung, fasilitas terbaik.",
                "Reguler": "Duduk di area reguler, kursi standar.",
                "Ekonomi": "Duduk di area ekonomi, kursi paling belakang."
            }
            info_posisi = posisi_duduk.get(jenis_tiket, "Jenis tiket tidak diketahui.")
            hasil += f"Info tempat duduk: {info_posisi}\n"
        else:
            hasil += "Kesimpulan: Status pembelian tiket tidak jelas.\n"

        if updated_facts.get("diskon"):
            hasil += f"Diskon yang didapat: {updated_facts['diskon']*100}%\n"
        else:
            hasil += "Anda tidak mendapatkan diskon.\n"

        hasil += "\nFakta lengkap:\n"
        for k, v in updated_facts.items():
            hasil += f"  {k}: {v}\n"

        self.text_summary.insert(tk.END, hasil)

class BackwardChainingPage(ttk.Frame):
    title = "Backward Chaining"
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Label(self, text="Backward Chaining", font=("Arial", 16)).pack(pady=10)
        
        ttk.Label(self, text="Masukkan umur:").pack()
        self.entry_umur = ttk.Entry(self)
        self.entry_umur.pack()
        
        self.var_member = tk.BooleanVar()
        self.chk_member = ttk.Checkbutton(self, text="Member?", variable=self.var_member)
        self.chk_member.pack()

        ttk.Label(self, text="Saldo (minimal 100):").pack()
        self.entry_saldo = ttk.Entry(self)
        self.entry_saldo.pack()

        self.var_blacklist = tk.BooleanVar()
        self.chk_blacklist = ttk.Checkbutton(self, text="Masuk daftar blacklist?", variable=self.var_blacklist)
        self.chk_blacklist.pack()

        self.var_tanggal_valid = tk.BooleanVar(value=True)
        self.chk_tanggal_valid = ttk.Checkbutton(self, text="Tanggal pembelian valid?", variable=self.var_tanggal_valid)
        self.chk_tanggal_valid.pack()

        ttk.Label(self, text="Jenis tiket:").pack()
        self.combo_jenis_tiket = ttk.Combobox(self, values=["VIP", "Reguler", "Ekonomi"])
        self.combo_jenis_tiket.pack()
        self.combo_jenis_tiket.current(0)
        
        ttk.Label(self, text="Pilih tujuan:").pack()
        self.combo_goal = ttk.Combobox(self, values=["bisa_beli_tiket", "diskon"])
        self.combo_goal.pack()
        self.combo_goal.current(0)

        ttk.Button(self, text="Proses", command=self.proses).pack(pady=10)

        # Frame hasil dua kolom
        self.frame_hasil = ttk.Frame(self)
        self.frame_hasil.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Label(self.frame_hasil, text="Aturan yang diterapkan:").grid(row=0, column=0, sticky="w")
        self.text_rules = tk.Text(self.frame_hasil, width=30, height=15)
        self.text_rules.grid(row=1, column=0, sticky="nsew", padx=(0,10))

        ttk.Label(self.frame_hasil, text="Kesimpulan dan Fakta:").grid(row=0, column=1, sticky="w")
        self.text_summary = tk.Text(self.frame_hasil, width=50, height=15)
        self.text_summary.grid(row=1, column=1, sticky="nsew")

        self.frame_hasil.columnconfigure(0, weight=1)
        self.frame_hasil.columnconfigure(1, weight=2)
        self.frame_hasil.rowconfigure(1, weight=1)

        ttk.Button(self, text="Kembali ke Menu Utama",
                   command=lambda: controller.show_frame(controller.homepage)).pack(pady=5)
    
    def backward_chaining(self, facts, goal):
        applied_rules = []

        if facts.get("blacklist", False):
            facts["bisa_beli_tiket"] = False
            facts["alasan_tidak_bisa"] = "Pengguna dalam daftar blacklist"
            if goal == "bisa_beli_tiket":
                applied_rules.append("rule5")
                return applied_rules, facts

        if not facts.get("tanggal_valid", True):
            facts["bisa_beli_tiket"] = False
            facts["alasan_tidak_bisa"] = "Tanggal pembelian tidak valid"
            if goal == "bisa_beli_tiket":
                applied_rules.append("rule6")
                return applied_rules, facts

        if facts.get("jenis_tiket") not in ["VIP", "Reguler", "Ekonomi"]:
            facts["bisa_beli_tiket"] = False
            facts["alasan_tidak_bisa"] = "Jenis tiket tidak valid"
            if goal == "bisa_beli_tiket":
                applied_rules.append("rule7")
                return applied_rules, facts

        if facts.get("saldo", 0) < 100.0:
            facts["bisa_beli_tiket"] = False
            facts["alasan_tidak_bisa"] = "Saldo tidak cukup"
            if goal == "bisa_beli_tiket":
                applied_rules.append("rule4")
                return applied_rules, facts

        if goal == "bisa_beli_tiket" and facts.get("umur", 0) > 17 and facts.get("bisa_beli_tiket", True) != False:
            facts["bisa_beli_tiket"] = True
            applied_rules.append("rule1")
            return applied_rules, facts
        
        if goal == "diskon" and facts.get("member", False):
            if "diskon" not in facts:
                facts["diskon"] = 0.1
            applied_rules.append("rule2")
            return applied_rules, facts

        return [], facts

    def proses(self):
        self.text_rules.delete("1.0", tk.END)
        self.text_summary.delete("1.0", tk.END)
        try:
            umur = int(self.entry_umur.get())
        except ValueError:
            messagebox.showerror("Error", "Umur harus berupa angka")
            return
        member = self.var_member.get()
        try:
            saldo = float(self.entry_saldo.get())
        except ValueError:
            messagebox.showerror("Error", "Saldo harus berupa angka")
            return
        blacklist = self.var_blacklist.get()
        tanggal_valid = self.var_tanggal_valid.get()
        jenis_tiket = self.combo_jenis_tiket.get()
        goal = self.combo_goal.get()

        facts = {
            "umur": umur,
            "member": member,
            "saldo": saldo,
            "blacklist": blacklist,
            "tanggal_valid": tanggal_valid,
            "jenis_tiket": jenis_tiket
        }

        applied_rules, updated_facts = self.backward_chaining(facts, goal)

        for rule in applied_rules:
            self.text_rules.insert(tk.END, f"- {rule}\n")

        hasil = ""
        if updated_facts.get("bisa_beli_tiket") == False:
            hasil += f"Tidak bisa membeli tiket karena: {updated_facts.get('alasan_tidak_bisa', 'Alasan tidak diketahui')}\n"
        elif updated_facts.get("bisa_beli_tiket"):
            hasil += "Kesimpulan: Anda bisa membeli tiket!\n"
            posisi_duduk = {
                "VIP": "Duduk di area VIP, dekat panggung, fasilitas terbaik.",
                "Reguler": "Duduk di area reguler, kursi standar.",
                "Ekonomi": "Duduk di area ekonomi, kursi paling belakang."
            }
            info_posisi = posisi_duduk.get(jenis_tiket, "Jenis tiket tidak diketahui.")
            hasil += f"Info tempat duduk: {info_posisi}\n"
        else:
            hasil += "Kesimpulan: Status pembelian tiket tidak jelas.\n"
        if updated_facts.get("diskon"):
            hasil += f"Diskon yang didapat: {updated_facts['diskon']*100}%\n"
        else:
            hasil += "Anda tidak mendapatkan diskon.\n"

        hasil += "\nFakta lengkap:\n"
        for k, v in updated_facts.items():
            hasil += f"  {k}: {v}\n"

        self.text_summary.insert(tk.END, hasil)


if __name__ == "__main__":
    app = ExpertSystemApp()
    app.mainloop()
