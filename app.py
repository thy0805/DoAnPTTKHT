import customtkinter as ctk
from tkinter import ttk
from modules.login import LoginFrame
from modules.pos import POSFrame
from modules.inventory import InventoryFrame
from modules.hr import HRFrame
from modules.promotions import PromotionsFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hệ Thống Quản Lý Cửa Hàng Thức Ăn Nhanh")
        self.geometry("1400x900")
        self.current_user = None
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
        
        self.show_login()

    def show_login(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.login_frame = LoginFrame(self, self.on_login_success)

    def on_login_success(self, user_info):
        self.current_user = user_info
        self.show_main_dashboard()

    def show_main_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(side="right", fill="both", expand=True)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=f"Xin chào,\n{self.current_user['TenNV']}", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(padx=20, pady=30)

        self.btn_pos = ctk.CTkButton(self.sidebar_frame, text="Bán Hàng (POS)", font=ctk.CTkFont(size=18, weight="bold"), height=50, command=lambda: self.show_frame(POSFrame))
        self.btn_pos.pack(padx=20, pady=15, fill="x")

        if self.current_user["VaiTro"] in ["QuanLy", "NhanVienKho"]:
            self.btn_inventory = ctk.CTkButton(self.sidebar_frame, text="Kho Hàng", font=ctk.CTkFont(size=18, weight="bold"), height=50, command=lambda: self.show_frame(InventoryFrame))
            self.btn_inventory.pack(padx=20, pady=15, fill="x")

        self.btn_hr = ctk.CTkButton(self.sidebar_frame, text="Nhân Sự & Chấm Công", font=ctk.CTkFont(size=18, weight="bold"), height=50, command=lambda: self.show_frame(HRFrame))
        self.btn_hr.pack(padx=20, pady=15, fill="x")

        if self.current_user["VaiTro"] == "QuanLy":
            self.btn_promo = ctk.CTkButton(self.sidebar_frame, text="Khuyến Mãi", font=ctk.CTkFont(size=18, weight="bold"), height=50, command=lambda: self.show_frame(PromotionsFrame))
            self.btn_promo.pack(padx=20, pady=15, fill="x")

        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Đăng Xuất", font=ctk.CTkFont(size=18, weight="bold"), height=50, fg_color="#C62828", hover_color="#B71C1C", command=self.logout)
        self.btn_logout.pack(padx=20, pady=20, side="bottom", fill="x")

        self.show_frame(POSFrame)

    def show_frame(self, frame_class):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        frame = frame_class(self.main_container, self.current_user)
        frame.pack(fill="both", expand=True)

    def logout(self):
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    app = App()
    app.mainloop()