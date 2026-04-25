import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
from database import lay_tat_ca_khuyen_mai, them_khuyen_mai

class PromotionsFrame(ctk.CTkFrame):
    def __init__(self, master, current_user):
        super().__init__(master, corner_radius=0)
        self.current_user = current_user
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        left_frame = ctk.CTkFrame(self, width=350, corner_radius=15)
        left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        left_frame.grid_propagate(False)
        
        ctk.CTkLabel(left_frame, text="THÊM KHUYẾN MÃI", font=("Arial", 24, "bold")).pack(pady=(20, 30))
        
        self.e_ten = ctk.CTkEntry(left_frame, placeholder_text="Tên chương trình KM", font=("Arial", 16), height=45)
        self.e_ten.pack(fill="x", padx=20, pady=10)
        
        self.c_ht = ctk.CTkComboBox(left_frame, values=["PhanTram", "TienMat"], font=("Arial", 16), height=45)
        self.c_ht.pack(fill="x", padx=20, pady=10)
        
        self.e_mg = ctk.CTkEntry(left_frame, placeholder_text="Mức giảm (vd: 10 hoặc 20000)", font=("Arial", 16), height=45)
        self.e_mg.pack(fill="x", padx=20, pady=10)
        
        self.e_dk = ctk.CTkEntry(left_frame, placeholder_text="Đơn hàng tối thiểu (VNĐ)", font=("Arial", 16), height=45)
        self.e_dk.pack(fill="x", padx=20, pady=10)
        
        self.e_bd = ctk.CTkEntry(left_frame, placeholder_text="Ngày bắt đầu (YYYY-MM-DD)", font=("Arial", 16), height=45)
        self.e_bd.pack(fill="x", padx=20, pady=10)
        
        self.e_kt = ctk.CTkEntry(left_frame, placeholder_text="Ngày kết thúc (YYYY-MM-DD)", font=("Arial", 16), height=45)
        self.e_kt.pack(fill="x", padx=20, pady=10)
        
        btn_add = ctk.CTkButton(left_frame, text="THÊM KHUYẾN MÃI", font=("Arial", 18, "bold"), height=55, fg_color="#1976D2", hover_color="#1565C0", command=self.add)
        btn_add.pack(fill="x", padx=20, pady=30)
        
        right_frame = ctk.CTkFrame(self, corner_radius=15)
        right_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        ctk.CTkLabel(right_frame, text="DANH SÁCH KHUYẾN MÃI", font=("Arial", 24, "bold")).pack(pady=(20, 15))
        
        columns = ("ID", "Ten", "HT", "Giam", "DK", "BD", "KT")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=20)
        self.tree.heading("ID", text="Mã KM")
        self.tree.heading("Ten", text="Tên Chương Trình")
        self.tree.heading("HT", text="Hình Thức")
        self.tree.heading("Giam", text="Mức Giảm")
        self.tree.heading("DK", text="Điều Kiện")
        self.tree.heading("BD", text="Bắt Đầu")
        self.tree.heading("KT", text="Kết Thúc")
        
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Ten", width=300)
        self.tree.column("HT", width=120, anchor="center")
        self.tree.column("Giam", width=120, anchor="e")
        self.tree.column("DK", width=150, anchor="e")
        self.tree.column("BD", width=120, anchor="center")
        self.tree.column("KT", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.load()

    def add(self):
        try:
            them_khuyen_mai(self.e_ten.get(), self.c_ht.get(), float(self.e_mg.get()), float(self.e_dk.get()), self.e_bd.get(), self.e_kt.get())
            self.load()
            messagebox.showinfo("Thành công", "Đã thêm chương trình khuyến mãi mới!")
            self.e_ten.delete(0, 'end')
            self.e_mg.delete(0, 'end')
            self.e_dk.delete(0, 'end')
            self.e_bd.delete(0, 'end')
            self.e_kt.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Lỗi", "Vui lòng kiểm tra lại thông tin nhập!")

    def load(self):
        for r in self.tree.get_children(): 
            self.tree.delete(r)
        for k in lay_tat_ca_khuyen_mai(): 
            self.tree.insert("", "end", values=(k.MaKM, k.TenKM, k.HinhThuc, f"{int(k.MucGiam):,}", f"{int(k.DieuKien):,}", k.NgayBatDau, k.NgayKetThuc))