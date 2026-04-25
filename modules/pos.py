import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
import os
from datetime import datetime
from database import lay_danh_sach_mon_an, tim_khach_hang, kiem_tra_khuyen_mai, lap_hoa_don, them_cthd, tich_diem, them_mon_an, sua_mon_an, xoa_mon_an, dang_ky_khach_hang, doi_diem_khach_hang, lay_danh_sach_khach_hang, lay_danh_sach_hoa_don, xem_chi_tiet_hoa_don

class POSFrame(ctk.CTkFrame):
    def __init__(self, master, current_user):
        super().__init__(master, corner_radius=0)
        self.current_user = current_user
        self.cart = []
        self.tong_tien = 0
        self.tien_giam_km = 0
        self.tien_giam_diem = 0
        self.ma_kh_chon = 1
        self.diem_khach_co = 0
        self.diem_su_dung = 0
        self.ma_km_chon = None

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_ban_hang = self.tabview.add("Bán Hàng")
        self.setup_ban_hang()
        
        self.tab_khach_hang = self.tabview.add("Quản Lý Khách Hàng")
        self.setup_khach_hang()

        self.tab_lich_su = self.tabview.add("Lịch Sử Hóa Đơn")
        self.setup_lich_su()

        if self.current_user["VaiTro"] == "QuanLy":
            self.tab_quan_ly_mon = self.tabview.add("Quản Lý Món Ăn")
            self.setup_quan_ly_mon()

        self.load_menu()

    def setup_ban_hang(self):
        self.tab_ban_hang.grid_columnconfigure(0, weight=5)
        self.tab_ban_hang.grid_columnconfigure(1, weight=5)
        self.tab_ban_hang.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self.tab_ban_hang)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(left_frame, text="THỰC ĐƠN", font=("Arial", 28, "bold")).pack(pady=15)

        cols = ("MaMon", "TenMon", "GiaBan")
        self.menu_table = ttk.Treeview(left_frame, columns=cols, show="headings")
        self.menu_table.heading("MaMon", text="Mã Món")
        self.menu_table.heading("TenMon", text="Tên Món")
        self.menu_table.heading("GiaBan", text="Đơn Giá")
        self.menu_table.column("MaMon", width=100, anchor="center")
        self.menu_table.column("TenMon", width=350)
        self.menu_table.column("GiaBan", width=150, anchor="e")
        self.menu_table.pack(fill="both", expand=True, padx=15, pady=10)
        self.menu_table.bind("<Double-1>", self.add_to_cart)

        right_frame = ctk.CTkScrollableFrame(self.tab_ban_hang)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(right_frame, text="GIỎ HÀNG", font=("Arial", 28, "bold")).pack(pady=15)

        self.cart_table = ttk.Treeview(right_frame, columns=("Ten", "SL", "Tien"), show="headings", height=8)
        self.cart_table.heading("Ten", text="Tên Món")
        self.cart_table.heading("SL", text="SL")
        self.cart_table.heading("Tien", text="Thành Tiền")
        self.cart_table.column("Ten", width=250)
        self.cart_table.column("SL", width=80, anchor="center")
        self.cart_table.column("Tien", width=150, anchor="e")
        self.cart_table.pack(fill="x", padx=15, pady=10)
        self.cart_table.bind("<Double-1>", self.remove_from_cart)

        info_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.sdt_kh = ctk.CTkEntry(info_frame, placeholder_text="SĐT Khách hàng", height=50, font=("Arial", 18))
        self.sdt_kh.pack(fill="x", pady=5)
        ctk.CTkButton(info_frame, text="Kiểm tra Khách & Khuyến Mãi", height=50, font=("Arial", 18, "bold"), command=self.check_km).pack(fill="x", pady=10)

        self.lbl_khach_hang = ctk.CTkLabel(info_frame, text="Khách: Khách vãng lai - Điểm: 0", font=("Arial", 18), text_color="#1976D2", wraplength=400, justify="right")
        self.lbl_khach_hang.pack(anchor="e", pady=5)

        diem_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        diem_frame.pack(fill="x", pady=5)
        self.entry_diem = ctk.CTkEntry(diem_frame, placeholder_text="Số điểm muốn dùng", height=40, font=("Arial", 16))
        self.entry_diem.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(diem_frame, text="Dùng Điểm", height=40, font=("Arial", 16, "bold"), command=self.ap_dung_diem).pack(side="right")

        self.lbl_tong = ctk.CTkLabel(info_frame, text="Tổng tiền: 0đ", font=("Arial", 20), justify="right", wraplength=400)
        self.lbl_tong.pack(anchor="e", pady=(10, 0))
        self.lbl_giam = ctk.CTkLabel(info_frame, text="Giảm KM: 0đ", font=("Arial", 20), text_color="#2E7D32", justify="right", wraplength=400)
        self.lbl_giam.pack(anchor="e", pady=2)
        self.lbl_tru_diem = ctk.CTkLabel(info_frame, text="Trừ Điểm: 0đ", font=("Arial", 20), text_color="#E65100", justify="right", wraplength=400)
        self.lbl_tru_diem.pack(anchor="e", pady=2)
        
        self.lbl_thanh_toan = ctk.CTkLabel(info_frame, text="Cần thanh toán: 0đ", font=("Arial", 28, "bold"), text_color="#D32F2F", justify="right", wraplength=400)
        self.lbl_thanh_toan.pack(anchor="e", pady=15)

        ctk.CTkButton(info_frame, text="THANH TOÁN", height=70, font=("Arial", 24, "bold"), fg_color="#2E7D32", hover_color="#1B5E20", command=self.checkout).pack(fill="x", side="bottom", pady=(20, 0))

    def add_to_cart(self, e):
        selected = self.menu_table.selection()
        if not selected: return
        item = self.menu_table.item(selected[0])['values']
        gia_tri = float(str(item[2]).replace(",", ""))

        found = False
        for c_item in self.cart:
            if c_item['id'] == item[0]:
                c_item['sl'] += 1
                c_item['tien'] += gia_tri
                found = True
                break

        if not found:
            self.cart.append({"id": item[0], "ten": item[1], "sl": 1, "gia": gia_tri, "tien": gia_tri})

        self.update_cart_ui()

    def update_cart_ui(self):
        for row in self.cart_table.get_children(): self.cart_table.delete(row)
        self.tong_tien = sum(item['tien'] for item in self.cart)
        for item in self.cart: 
            self.cart_table.insert("", "end", values=(item['ten'], item['sl'], f"{int(item['tien']):,}"))
        self.lbl_tong.configure(text=f"Tổng tiền: {int(self.tong_tien):,}đ")
        self.recalc_total()

    def remove_from_cart(self, e):
        selected = self.cart_table.selection()
        if not selected: return
        idx = self.cart_table.index(selected[0])
        item = self.cart[idx]
        
        if item['sl'] > 1:
            item['sl'] -= 1
            item['tien'] -= item['gia']
        else:
            self.cart.pop(idx)
            
        self.update_cart_ui()

    def setup_khach_hang(self):
        btn_frame = ctk.CTkFrame(self.tab_khach_hang, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Đăng Ký Khách Hàng Mới", font=("Arial", 18, "bold"), height=50, command=lambda: self.open_register_kh_popup("")).pack(side="left")
        ctk.CTkButton(btn_frame, text="Làm Mới Danh Sách", font=("Arial", 18, "bold"), height=50, command=self.load_khach_hang).pack(side="left", padx=10)

        cols = ("MaKH", "TenKH", "SDT", "Diem", "NgayDK")
        self.kh_table = ttk.Treeview(self.tab_khach_hang, columns=cols, show="headings")
        self.kh_table.heading("MaKH", text="Mã KH")
        self.kh_table.heading("TenKH", text="Tên Khách Hàng")
        self.kh_table.heading("SDT", text="Số Điện Thoại")
        self.kh_table.heading("Diem", text="Điểm Tích Lũy")
        self.kh_table.heading("NgayDK", text="Ngày Đăng Ký")
        self.kh_table.column("MaKH", width=100, anchor="center")
        self.kh_table.column("TenKH", width=350)
        self.kh_table.column("SDT", width=200, anchor="center")
        self.kh_table.column("Diem", width=150, anchor="center")
        self.kh_table.column("NgayDK", width=200, anchor="center")
        self.kh_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_khach_hang()

    def load_khach_hang(self):
        for row in self.kh_table.get_children(): self.kh_table.delete(row)
        for kh in lay_danh_sach_khach_hang():
            sdt_str = '0' + str(kh.SoDienThoai) if not str(kh.SoDienThoai).startswith('0') else str(kh.SoDienThoai)
            self.kh_table.insert("", "end", values=(kh.MaKH, kh.TenKH, sdt_str, kh.DiemTichLuy, kh.NgayDangKy))

    def setup_lich_su(self):
        btn_frame = ctk.CTkFrame(self.tab_lich_su, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Làm Mới Danh Sách", font=("Arial", 18, "bold"), height=50, command=self.load_lich_su).pack(side="left")

        cols = ("ID", "Ngay", "NV", "KH", "Tong")
        self.history_table = ttk.Treeview(self.tab_lich_su, columns=cols, show="headings")
        self.history_table.heading("ID", text="Mã HD")
        self.history_table.heading("Ngay", text="Ngày Lập")
        self.history_table.heading("NV", text="Nhân Viên")
        self.history_table.heading("KH", text="Khách Hàng")
        self.history_table.heading("Tong", text="Thanh Toán")
        
        self.history_table.column("ID", width=80, anchor="center")
        self.history_table.column("Ngay", width=200, anchor="center")
        self.history_table.column("NV", width=200)
        self.history_table.column("KH", width=200)
        self.history_table.column("Tong", width=150, anchor="e")
        
        self.history_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.history_table.bind("<Double-1>", self.show_hd_detail)
        
        self.load_lich_su()

    def load_lich_su(self):
        for row in self.history_table.get_children(): self.history_table.delete(row)
        for hd in lay_danh_sach_hoa_don():
            self.history_table.insert("", "end", values=(hd[0], hd[1].strftime("%Y-%m-%d %H:%M"), hd[2], hd[3], f"{int(hd[4]):,}"))

    def show_hd_detail(self, e):
        selected = self.history_table.selection()
        if not selected: return
        ma_hd = self.history_table.item(selected[0])['values'][0]
        chi_tiet = xem_chi_tiet_hoa_don(ma_hd)
        
        popup = ctk.CTkToplevel(self)
        popup.title(f"Chi Tiết Hóa Đơn #{ma_hd}")
        popup.geometry("600x400")
        popup.grab_set()
        
        cols = ("Ten", "SL", "Gia", "ThanhTien")
        table = ttk.Treeview(popup, columns=cols, show="headings")
        table.heading("Ten", text="Tên Món")
        table.heading("SL", text="SL")
        table.heading("Gia", text="Đơn Giá")
        table.heading("ThanhTien", text="Thành Tiền")
        
        table.column("Ten", width=200)
        table.column("SL", width=50, anchor="center")
        table.column("Gia", width=100, anchor="e")
        table.column("ThanhTien", width=120, anchor="e")
        table.pack(fill="both", expand=True, padx=20, pady=20)
        
        for item in chi_tiet:
            table.insert("", "end", values=(item[1], item[2], f"{int(item[3]):,}", f"{int(item[4]):,}"))

    def setup_quan_ly_mon(self):
        btn_frame = ctk.CTkFrame(self.tab_quan_ly_mon, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Thêm Món Ăn Mới", font=("Arial", 18, "bold"), height=50, command=self.open_add_mon_popup).pack(side="left")

        cols = ("MaMon", "TenMon", "GiaBan")
        self.ql_menu_table = ttk.Treeview(self.tab_quan_ly_mon, columns=cols, show="headings")
        self.ql_menu_table.heading("MaMon", text="Mã Món")
        self.ql_menu_table.heading("TenMon", text="Tên Món Ăn")
        self.ql_menu_table.heading("GiaBan", text="Giá Bán")
        self.ql_menu_table.column("MaMon", width=150, anchor="center")
        self.ql_menu_table.column("TenMon", width=500)
        self.ql_menu_table.column("GiaBan", width=250, anchor="e")
        self.ql_menu_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.ql_menu_table.bind("<Double-1>", self.open_edit_mon_popup)

    def load_menu(self):
        for row in self.menu_table.get_children(): self.menu_table.delete(row)
        if hasattr(self, 'ql_menu_table'):
            for row in self.ql_menu_table.get_children(): self.ql_menu_table.delete(row)

        for mon in lay_danh_sach_mon_an():
            self.menu_table.insert("", "end", values=(mon.MaMon, mon.TenMon, f"{int(mon.GiaBan):,}"))
            if hasattr(self, 'ql_menu_table'):
                self.ql_menu_table.insert("", "end", values=(mon.MaMon, mon.TenMon, f"{int(mon.GiaBan):,}"))

    def check_km(self):
        sdt = self.sdt_kh.get()
        self.ma_kh_chon = 1
        self.diem_khach_co = 0
        self.diem_su_dung = 0
        self.tien_giam_diem = 0
        self.entry_diem.delete(0, 'end')
        self.lbl_khach_hang.configure(text="Khách: Khách vãng lai - Điểm: 0")
        
        if sdt:
            kh = tim_khach_hang(sdt)
            if kh:
                self.ma_kh_chon = kh.MaKH
                self.diem_khach_co = kh.DiemTichLuy
                self.lbl_khach_hang.configure(text=f"Khách: {kh.TenKH} - Điểm: {self.diem_khach_co}")
            else:
                if messagebox.askyesno("Khách Mới", "Chưa có khách hàng này. Bạn có muốn đăng ký mới không?"):
                    self.open_register_kh_popup(sdt)
        self.recalc_total()

    def ap_dung_diem(self):
        if self.ma_kh_chon == 1:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khách hàng thành viên để dùng điểm!")
            return
        try:
            diem_nhap = int(self.entry_diem.get())
            if diem_nhap > self.diem_khach_co:
                messagebox.showerror("Lỗi", "Khách hàng không đủ điểm!")
                return
            if diem_nhap < 0: return
            
            self.diem_su_dung = diem_nhap
            self.tien_giam_diem = self.diem_su_dung * 1000 
            self.recalc_total()
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số điểm hợp lệ!")

    def open_register_kh_popup(self, sdt):
        popup = ctk.CTkToplevel(self)
        popup.title("Đăng Ký Khách Hàng")
        popup.geometry("450x350")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Tên Khách Hàng:", font=("Arial", 18)).pack(pady=(30, 5))
        e_ten = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_ten.pack(pady=5)

        ctk.CTkLabel(popup, text="Số Điện Thoại:", font=("Arial", 18)).pack(pady=5)
        e_sdt = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_sdt.insert(0, sdt)
        e_sdt.pack(pady=5)

        def save():
            try:
                ma_kh = dang_ky_khach_hang(e_ten.get(), e_sdt.get())
                self.ma_kh_chon = ma_kh
                self.diem_khach_co = 0
                self.lbl_khach_hang.configure(text=f"Khách: {e_ten.get()} - Điểm: 0")
                self.load_khach_hang()
                popup.destroy()
                messagebox.showinfo("Thành công", "Đã đăng ký khách hàng mới!")
            except:
                messagebox.showerror("Lỗi", "Không thể đăng ký, vui lòng kiểm tra lại thông tin!")

        ctk.CTkButton(popup, text="Đăng Ký", font=("Arial", 18, "bold"), height=50, command=save).pack(pady=30)

    def recalc_total(self):
        self.tien_giam_km = 0
        self.ma_km_chon = None
        if self.tong_tien > 0:
            km = kiem_tra_khuyen_mai(self.tong_tien)
            if km:
                self.ma_km_chon = km.MaKM
                self.tien_giam_km = self.tong_tien * (float(km.MucGiam)/100) if km.HinhThuc == "PhanTram" else float(km.MucGiam)
                self.lbl_giam.configure(text=f"Giảm KM: {int(self.tien_giam_km):,}đ\n({km.TenKM})")
            else:
                self.lbl_giam.configure(text="Giảm KM: 0đ")
                
        self.lbl_tru_diem.configure(text=f"Trừ Điểm: {int(self.tien_giam_diem):,}đ")
        
        can_thanh_toan = self.tong_tien - self.tien_giam_km - self.tien_giam_diem
        if can_thanh_toan < 0: can_thanh_toan = 0
        
        self.lbl_thanh_toan.configure(text=f"Cần thanh toán: {int(can_thanh_toan):,}đ")

    def checkout(self):
        if not self.cart: return
        
        can_thanh_toan = self.tong_tien - self.tien_giam_km - self.tien_giam_diem
        if can_thanh_toan < 0: can_thanh_toan = 0
        
        tong_giam = self.tien_giam_km + self.tien_giam_diem
        
        mahd = lap_hoa_don(self.current_user['MaNV'], self.ma_kh_chon, self.ma_km_chon, self.tong_tien, tong_giam, can_thanh_toan)
        
        if self.diem_su_dung > 0 and self.ma_kh_chon != 1:
            doi_diem_khach_hang(self.ma_kh_chon, self.diem_su_dung)
            self.diem_khach_co -= self.diem_su_dung
        
        hd_text = f"===== HOÁ ĐƠN THANH TOÁN =====\n"
        hd_text += f"Mã HD: {mahd}\n"
        hd_text += f"Ngày: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        hd_text += f"Thu ngân: {self.current_user['TenNV']}\n"
        hd_text += f"------------------------------\n"
        
        for item in self.cart:
            them_cthd(mahd, item['id'], item['sl'], item['gia'])
            hd_text += f"{item['ten']} x{item['sl']}: {int(item['tien']):,}đ\n"
            
        if self.ma_kh_chon != 1:
            diem_cong = int(can_thanh_toan/10000) 
            tich_diem(self.ma_kh_chon, diem_cong)
            hd_text += f"------------------------------\n"
            hd_text += f"Khách hàng số: {self.ma_kh_chon}\n"
            hd_text += f"Sử dụng điểm: -{self.diem_su_dung} điểm\n"
            hd_text += f"Điểm cộng thêm: +{diem_cong} điểm\n"

        hd_text += f"------------------------------\n"
        hd_text += f"Tổng tiền: {int(self.tong_tien):,}đ\n"
        hd_text += f"Giảm giá KM: {int(self.tien_giam_km):,}đ\n"
        hd_text += f"Trừ điểm: {int(self.tien_giam_diem):,}đ\n"
        hd_text += f"Thành tiền: {int(can_thanh_toan):,}đ\n"
        hd_text += f"==============================\n"

        if not os.path.exists("HoaDon"):
            os.makedirs("HoaDon")
        
        file_path = f"HoaDon/HD_{mahd}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(hd_text)

        messagebox.showinfo("Thành công", f"Đã thanh toán và in hóa đơn tại:\n{file_path}")
        
        self.cart, self.tong_tien, self.tien_giam_km, self.tien_giam_diem = [], 0, 0, 0
        self.diem_su_dung = 0
        self.ma_km_chon = None
        self.sdt_kh.delete(0, 'end')
        self.entry_diem.delete(0, 'end')
        self.lbl_khach_hang.configure(text="Khách: Khách vãng lai - Điểm: 0")
        self.update_cart_ui()
        self.lbl_giam.configure(text="Giảm KM: 0đ")
        self.lbl_tru_diem.configure(text="Trừ Điểm: 0đ")
        self.load_khach_hang()
        self.load_lich_su()

    def open_add_mon_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Thêm Món Ăn Mới")
        popup.geometry("450x350")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Tên món ăn:", font=("Arial", 18)).pack(pady=(30, 5))
        e_ten = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_ten.pack(pady=5)

        ctk.CTkLabel(popup, text="Giá bán:", font=("Arial", 18)).pack(pady=5)
        e_gia = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_gia.pack(pady=5)

        def save():
            try:
                them_mon_an(e_ten.get(), float(e_gia.get()))
                self.load_menu()
                popup.destroy()
                messagebox.showinfo("Thành công", "Đã thêm món ăn!")
            except:
                messagebox.showerror("Lỗi", "Vui lòng kiểm tra lại thông tin nhập!")

        ctk.CTkButton(popup, text="Lưu", font=("Arial", 18, "bold"), height=50, command=save).pack(pady=30)

    def open_edit_mon_popup(self, e):
        selected = self.ql_menu_table.selection()
        if not selected: return
        item = self.ql_menu_table.item(selected[0])['values']

        popup = ctk.CTkToplevel(self)
        popup.title("Cập Nhật Món Ăn")
        popup.geometry("450x450")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Mã món:", font=("Arial", 18)).pack(pady=(20, 5))
        e_ma = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_ma.insert(0, item[0])
        e_ma.configure(state="readonly")
        e_ma.pack(pady=5)

        ctk.CTkLabel(popup, text="Tên món ăn:", font=("Arial", 18)).pack(pady=5)
        e_ten = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_ten.insert(0, item[1])
        e_ten.pack(pady=5)

        ctk.CTkLabel(popup, text="Giá bán:", font=("Arial", 18)).pack(pady=5)
        e_gia = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_gia.insert(0, str(item[2]).replace(",", ""))
        e_gia.pack(pady=5)

        def update():
            try:
                sua_mon_an(int(e_ma.get()), e_ten.get(), float(e_gia.get()))
                self.load_menu()
                popup.destroy()
                messagebox.showinfo("Thành công", "Đã cập nhật món ăn!")
            except:
                messagebox.showerror("Lỗi", "Vui lòng kiểm tra lại thông tin nhập!")

        def delete():
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa món này?"):
                xoa_mon_an(int(e_ma.get()))
                self.load_menu()
                popup.destroy()

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="Cập Nhật", font=("Arial", 18, "bold"), height=50, fg_color="#F57C00", command=update).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Xóa", font=("Arial", 18, "bold"), height=50, fg_color="#D32F2F", command=delete).pack(side="left", padx=10)