import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox
import os
from datetime import datetime
from database import lay_nguyen_lieu, lay_danh_sach_nha_cung_cap, lay_tat_ca_nguyen_lieu, lap_phieu_nhap_kho, them_chi_tiet_nhap_kho, them_nha_cung_cap, them_nguyen_lieu, lay_lich_su_nhap_kho, xem_chi_tiet_phieu_nhap

class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master, current_user):
        super().__init__(master, corner_radius=0)
        self.current_user = current_user
        self.danh_sach_nhap = []
        
        self.full_ncc_list = []
        self.full_nl_list = []

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_ton_kho = self.tabview.add("Tồn Kho & Kiểm Kê")
        self.tab_lich_su = self.tabview.add("Lịch Sử Nhập Kho")

        self.setup_ton_kho()
        self.setup_lich_su()

    def setup_ton_kho(self):
        top_frame = ctk.CTkFrame(self.tab_ton_kho, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(top_frame, text="KHO HÀNG & KIỂM KÊ", font=("Arial", 24, "bold")).pack(side="left")
        
        btn_nhap = ctk.CTkButton(top_frame, text="TẠO PHIẾU NHẬP KHO", font=("Arial", 16, "bold"), height=45, fg_color="#1976D2", command=self.open_phieu_nhap_popup)
        btn_nhap.pack(side="right", padx=10)

        btn_refresh = ctk.CTkButton(top_frame, text="Làm mới", font=("Arial", 16, "bold"), height=45, command=self.load_ton_kho)
        btn_refresh.pack(side="right", padx=10)

        columns = ("MaNL", "TenNL", "DonVi", "SoLuongTon")
        self.stock_table = ttk.Treeview(self.tab_ton_kho, columns=columns, show="headings")
        self.stock_table.heading("MaNL", text="Mã NL")
        self.stock_table.heading("TenNL", text="Tên Nguyên Liệu")
        self.stock_table.heading("DonVi", text="Đơn Vị Tính")
        self.stock_table.heading("SoLuongTon", text="Số Lượng Tồn")
        
        self.stock_table.column("MaNL", width=100, anchor="center")
        self.stock_table.column("TenNL", width=400)
        self.stock_table.column("DonVi", width=150, anchor="center")
        self.stock_table.column("SoLuongTon", width=150, anchor="center")
        self.stock_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.load_ton_kho()

    def load_ton_kho(self):
        for row in self.stock_table.get_children():
            self.stock_table.delete(row)
        for nl in lay_nguyen_lieu():
            self.stock_table.insert("", "end", values=(nl.MaNL, nl.TenNL, nl.DonViTinh, nl.SoLuongTon))

    def setup_lich_su(self):
        btn_frame = ctk.CTkFrame(self.tab_lich_su, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Làm Mới Danh Sách", font=("Arial", 16, "bold"), height=45, command=self.load_lich_su).pack(side="left")

        cols = ("ID", "Ngay", "NV", "NCC", "TongTien", "TrangThai")
        self.history_table = ttk.Treeview(self.tab_lich_su, columns=cols, show="headings")
        self.history_table.heading("ID", text="Mã Phiếu")
        self.history_table.heading("Ngay", text="Ngày Nhập")
        self.history_table.heading("NV", text="Người Lập")
        self.history_table.heading("NCC", text="Nhà Cung Cấp")
        self.history_table.heading("TongTien", text="Tổng Tiền")
        self.history_table.heading("TrangThai", text="Trạng Thái")
        
        self.history_table.column("ID", width=80, anchor="center")
        self.history_table.column("Ngay", width=180, anchor="center")
        self.history_table.column("NV", width=200)
        self.history_table.column("NCC", width=250)
        self.history_table.column("TongTien", width=150, anchor="e")
        self.history_table.column("TrangThai", width=150, anchor="center")
        
        self.history_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.history_table.bind("<Double-1>", self.show_pn_detail)
        
        self.load_lich_su()

    def load_lich_su(self):
        for row in self.history_table.get_children(): self.history_table.delete(row)
        for pn in lay_lich_su_nhap_kho():
            self.history_table.insert("", "end", values=(pn[0], pn[1].strftime("%Y-%m-%d %H:%M"), pn[2], pn[3], f"{int(pn[4]):,}", pn[5]))

    def show_pn_detail(self, e):
        selected = self.history_table.selection()
        if not selected: return
        
        item = self.history_table.item(selected[0])['values']
        ma_pn, ngay_lap, nguoi_lap, ten_ncc = item[0], item[1], item[2], item[3]
        chi_tiet = xem_chi_tiet_phieu_nhap(ma_pn)
        
        popup = ctk.CTkToplevel(self)
        popup.title(f"Chi Tiết Phiếu Nhập Kho #{ma_pn}")
        popup.geometry("700x500")
        popup.grab_set()
        
        info_frame = ctk.CTkFrame(popup, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(info_frame, text=f"Mã phiếu: {ma_pn}  |  Ngày lập: {ngay_lap}", font=("Arial", 16)).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Nhà cung cấp: {ten_ncc}", font=("Arial", 16, "bold"), text_color="#1976D2").pack(anchor="w", pady=5)
        ctk.CTkLabel(info_frame, text=f"Người lập: {nguoi_lap}", font=("Arial", 16)).pack(anchor="w")

        cols = ("Ten", "SL", "Gia", "ThanhTien")
        table = ttk.Treeview(popup, columns=cols, show="headings")
        table.heading("Ten", text="Tên Nguyên Liệu")
        table.heading("SL", text="Số Lượng")
        table.heading("Gia", text="Đơn Giá")
        table.heading("ThanhTien", text="Thành Tiền")
        
        table.column("Ten", width=250)
        table.column("SL", width=80, anchor="center")
        table.column("Gia", width=120, anchor="e")
        table.column("ThanhTien", width=150, anchor="e")
        table.pack(fill="both", expand=True, padx=20, pady=10)
        
        for ct in chi_tiet:
            table.insert("", "end", values=(ct[0], ct[1], f"{int(ct[2]):,}", f"{int(ct[3]):,}"))
            
        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        def in_lai_phieu():
            text = f"===== PHIẾU NHẬP KHO =====\n"
            text += f"Mã Phiếu: {ma_pn} (Bản In Lại)\n"
            text += f"Ngày lập: {ngay_lap}\n"
            text += f"Người lập: {nguoi_lap}\n"
            text += f"Nhà Cung Cấp: {ten_ncc}\n"
            text += f"------------------------------\n"
            tong_tien = 0
            for ct in chi_tiet:
                text += f"{ct[0]} x{ct[1]}: {int(ct[3]):,}đ\n"
                tong_tien += ct[3]
            text += f"------------------------------\n"
            text += f"Tổng cộng: {int(tong_tien):,}đ\n"
            text += f"==============================\n"
            
            if not os.path.exists("PhieuNhap"):
                os.makedirs("PhieuNhap")
            file_path = f"PhieuNhap/PN_{ma_pn}_Reprint.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Thành công", f"Đã xuất lại phiếu nhập tại:\n{file_path}")

        ctk.CTkButton(btn_frame, text="In Lại Phiếu", font=("Arial", 16, "bold"), height=45, fg_color="#F57C00", command=in_lai_phieu).pack()

    def fetch_lists(self):
        self.full_ncc_list = [f"{n[0]} - {n[1]}" for n in lay_danh_sach_nha_cung_cap()]
        self.full_nl_list = [f"{n[0]} - {n[1]}" for n in lay_tat_ca_nguyen_lieu()]

    def open_phieu_nhap_popup(self):
        self.fetch_lists()
        self.danh_sach_nhap = []
        
        popup = ctk.CTkToplevel(self)
        popup.title("Tạo Phiếu Nhập Kho")
        popup.geometry("1100x750")
        popup.grab_set()

        form_frame = ctk.CTkFrame(popup, fg_color="transparent")
        form_frame.pack(fill="x", pady=15, padx=15)

        ctk.CTkLabel(form_frame, text="Nhà cung cấp:", font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.cb_ncc = ctk.CTkComboBox(form_frame, font=("Arial", 18), width=400, height=45, values=self.full_ncc_list)
        self.cb_ncc.grid(row=0, column=1, padx=10, pady=10, sticky="w", columnspan=3)
        self.cb_ncc.bind("<KeyRelease>", lambda e: self.live_search(self.cb_ncc, self.full_ncc_list))

        btn_add_ncc = ctk.CTkButton(form_frame, text="+ Thêm NCC", font=("Arial", 16, "bold"), height=45, width=120, command=self.open_add_ncc_popup)
        btn_add_ncc.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(form_frame, text="Nguyên liệu:", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.cb_nl = ctk.CTkComboBox(form_frame, font=("Arial", 18), width=400, height=45, values=self.full_nl_list)
        self.cb_nl.grid(row=1, column=1, padx=10, pady=10, sticky="w", columnspan=3)
        self.cb_nl.bind("<KeyRelease>", lambda e: self.live_search(self.cb_nl, self.full_nl_list))

        btn_add_nl_new = ctk.CTkButton(form_frame, text="+ Thêm NL", font=("Arial", 16, "bold"), height=45, width=120, command=self.open_add_nl_popup)
        btn_add_nl_new.grid(row=1, column=4, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(form_frame, text="Số lượng:", font=("Arial", 18)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_sl = ctk.CTkEntry(form_frame, font=("Arial", 18), width=150, height=45)
        self.entry_sl.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(form_frame, text="Đơn giá:", font=("Arial", 18)).grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.entry_gia = ctk.CTkEntry(form_frame, font=("Arial", 18), width=180, height=45)
        self.entry_gia.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        btn_add_nl = ctk.CTkButton(form_frame, text="Thêm vào danh sách", font=("Arial", 18, "bold"), height=45, command=self.them_vao_danh_sach)
        btn_add_nl.grid(row=2, column=4, padx=20, pady=10, sticky="w")

        cols = ("MaNL", "TenNL", "SoLuong", "DonGia", "ThanhTien")
        self.import_table = ttk.Treeview(popup, columns=cols, show="headings")
        self.import_table.heading("MaNL", text="Mã NL")
        self.import_table.heading("TenNL", text="Tên Nguyên Liệu")
        self.import_table.heading("SoLuong", text="Số Lượng")
        self.import_table.heading("DonGia", text="Đơn Giá")
        self.import_table.heading("ThanhTien", text="Thành Tiền")
        self.import_table.column("MaNL", width=100, anchor="center")
        self.import_table.column("TenNL", width=350)
        self.import_table.column("SoLuong", width=150, anchor="center")
        self.import_table.column("DonGia", width=200, anchor="e")
        self.import_table.column("ThanhTien", width=200, anchor="e")
        self.import_table.pack(fill="both", expand=True, padx=20, pady=10)

        self.lbl_tong_nhap = ctk.CTkLabel(popup, text="Tổng tiền: 0đ", font=("Arial", 28, "bold"), text_color="#D32F2F")
        self.lbl_tong_nhap.pack(anchor="e", padx=20, pady=10)

        btn_submit = ctk.CTkButton(popup, text="HOÀN TẤT VÀ IN PHIẾU", font=("Arial", 24, "bold"), fg_color="#2E7D32", height=70, command=lambda: self.tao_phieu_nhap(popup))
        btn_submit.pack(fill="x", padx=20, pady=(10, 20))

    def live_search(self, widget, full_list):
        typed = widget.get().lower()
        filtered = [x for x in full_list if typed in x.lower()]
        widget.configure(values=filtered)

    def open_add_ncc_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Thêm Nhà Cung Cấp Mới")
        popup.geometry("450x400")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Tên Nhà Cung Cấp:", font=("Arial", 18)).pack(pady=(30, 5))
        e_ten = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_ten.pack(pady=5)

        ctk.CTkLabel(popup, text="Số Điện Thoại:", font=("Arial", 18)).pack(pady=5)
        e_sdt = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_sdt.pack(pady=5)

        ctk.CTkLabel(popup, text="Địa Chỉ:", font=("Arial", 18)).pack(pady=5)
        e_dc = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_dc.pack(pady=5)

        def save():
            try:
                them_nha_cung_cap(e_ten.get(), e_sdt.get(), e_dc.get())
                self.fetch_lists()
                self.cb_ncc.configure(values=self.full_ncc_list)
                self.cb_ncc.set(self.full_ncc_list[-1])
                popup.destroy()
                messagebox.showinfo("Thành công", "Đã thêm nhà cung cấp mới!")
            except:
                messagebox.showerror("Lỗi", "Vui lòng kiểm tra lại thông tin nhập!")

        ctk.CTkButton(popup, text="Lưu", font=("Arial", 18, "bold"), height=50, command=save).pack(pady=30)

    def open_add_nl_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Thêm Nguyên Liệu Mới")
        popup.geometry("450x300")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Tên Nguyên Liệu:", font=("Arial", 18)).pack(pady=(30, 5))
        e_ten = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_ten.pack(pady=5)

        ctk.CTkLabel(popup, text="Đơn vị tính (Kg, Lít,...):", font=("Arial", 18)).pack(pady=5)
        e_dv = ctk.CTkEntry(popup, font=("Arial", 18), width=300, height=50)
        e_dv.pack(pady=5)

        def save():
            try:
                them_nguyen_lieu(e_ten.get(), e_dv.get())
                self.fetch_lists()
                self.cb_nl.configure(values=self.full_nl_list)
                self.cb_nl.set(self.full_nl_list[-1])
                popup.destroy()
                messagebox.showinfo("Thành công", "Đã thêm nguyên liệu mới!")
            except:
                messagebox.showerror("Lỗi", "Vui lòng kiểm tra lại thông tin nhập!")

        ctk.CTkButton(popup, text="Lưu", font=("Arial", 18, "bold"), height=50, command=save).pack(pady=30)

    def them_vao_danh_sach(self):
        nl_str = self.cb_nl.get()
        if not nl_str or "-" not in nl_str: return
        try:
            sl = int(self.entry_sl.get())
            gia = float(self.entry_gia.get())
            ma_nl = int(nl_str.split(" - ")[0])
            ten_nl = nl_str.split(" - ")[1]
            thanh_tien = sl * gia
            
            self.danh_sach_nhap.append({"MaNL": ma_nl, "TenNL": ten_nl, "SoLuong": sl, "DonGia": gia, "ThanhTien": thanh_tien})
            self.cap_nhat_bang_nhap()
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng số lượng và đơn giá bằng số!")

    def cap_nhat_bang_nhap(self):
        for row in self.import_table.get_children(): self.import_table.delete(row)
        tong = 0
        for item in self.danh_sach_nhap:
            tong += item["ThanhTien"]
            self.import_table.insert("", "end", values=(item["MaNL"], item["TenNL"], item["SoLuong"], f"{int(item['DonGia']):,}", f"{int(item['ThanhTien']):,}"))
        self.lbl_tong_nhap.configure(text=f"Tổng tiền: {int(tong):,}đ")

    def tao_phieu_nhap(self, popup):
        ncc_str = self.cb_ncc.get()
        if not ncc_str or "-" not in ncc_str or not self.danh_sach_nhap:
            messagebox.showerror("Lỗi", "Vui lòng chọn Nhà Cung Cấp hợp lệ và thêm nguyên liệu!")
            return
        try:
            ma_ncc = int(ncc_str.split(" - ")[0])
            tong_tien = sum(item["ThanhTien"] for item in self.danh_sach_nhap)
            
            thoi_gian_hien_tai = datetime.now()
            thoi_gian_str = thoi_gian_hien_tai.strftime('%Y-%m-%d %H:%M:%S')
            
            ma_pn = lap_phieu_nhap_kho(self.current_user["MaNV"], ma_ncc, tong_tien)
            for item in self.danh_sach_nhap:
                them_chi_tiet_nhap_kho(ma_pn, item["MaNL"], item["SoLuong"], item["DonGia"])
            
            pn_text = f"===== PHIẾU NHẬP KHO =====\n"
            pn_text += f"Mã Phiếu: {ma_pn}\n"
            pn_text += f"Ngày lập: {thoi_gian_str}\n"
            pn_text += f"Người lập: {self.current_user['TenNV']}\n"
            pn_text += f"Nhà Cung Cấp: {ncc_str.split(' - ')[1]}\n"
            pn_text += f"------------------------------\n"
            
            for item in self.danh_sach_nhap:
                pn_text += f"{item['TenNL']} x{item['SoLuong']}: {int(item['ThanhTien']):,}đ\n"
                
            pn_text += f"------------------------------\n"
            pn_text += f"Tổng cộng: {int(tong_tien):,}đ\n"
            pn_text += f"==============================\n"
            
            if not os.path.exists("PhieuNhap"):
                os.makedirs("PhieuNhap")
            
            file_path = f"PhieuNhap/PN_{ma_pn}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(pn_text)
            
            messagebox.showinfo("Thành công", f"Đã tạo và in phiếu nhập kho tại:\n{file_path}")
            popup.destroy()
            self.load_ton_kho()
            self.load_lich_su()
        except Exception as e:
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi tạo phiếu nhập kho!")