import customtkinter as ctk
import tkinter.messagebox as messagebox
from database import dang_nhap

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, login_success_callback):
        super().__init__(master)
        self.login_success_callback = login_success_callback
        self.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self, text="ĐĂNG NHẬP HỆ THỐNG", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(padx=40, pady=(30, 20))

        self.phone_entry = ctk.CTkEntry(self, placeholder_text="Số điện thoại", width=300, height=40)
        self.phone_entry.pack(padx=40, pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Mật khẩu", show="*", width=300, height=40)
        self.password_entry.pack(padx=40, pady=10)

        self.login_button = ctk.CTkButton(self, text="Đăng Nhập", command=self.handle_login, width=300, height=45, font=ctk.CTkFont(size=16, weight="bold"))
        self.login_button.pack(padx=40, pady=(20, 30))

    def handle_login(self):
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        if not phone or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        user = dang_nhap(phone, password)
        if user:
            user_info = {"MaNV": user.MaNV, "TenNV": user.TenNV, "VaiTro": user.VaiTro}
            self.login_success_callback(user_info)
        else:
            messagebox.showerror("Lỗi", "Sai số điện thoại hoặc mật khẩu!")