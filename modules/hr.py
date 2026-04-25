import customtkinter as ctk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageDraw, ImageFont
import tkinter.messagebox as messagebox
import threading
import face_recognition
from face_utils import check_liveness, get_face_embedding, compare_faces
from database import cham_cong_vao, cham_cong_ra, lay_danh_sach_nhan_vien, them_nhan_vien, sua_nhan_vien, xoa_nhan_vien, lay_lich_su_cham_cong, lay_tat_ca_khuon_mat

class HRFrame(ctk.CTkFrame):
    def __init__(self, master, current_user):
        super().__init__(master, corner_radius=0)
        self.current_user = current_user
        self.cap = None
        self.is_processing_face = False

        self.tabview = ctk.CTkTabview(self, corner_radius=15, border_width=2, border_color="#D1D9E6")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.setup_cham_cong_tab()
        if self.current_user["VaiTro"] == "QuanLy": 
            self.setup_quan_ly_tab()
            self.setup_lich_su_tab()

    def setup_cham_cong_tab(self):
        self.tab_cc = self.tabview.add("Chấm Công FaceID")
        self.build_live_ui()

    def build_live_ui(self):
        for widget in self.tab_cc.winfo_children():
            widget.destroy()

        self.lbl_cam = ctk.CTkLabel(self.tab_cc, text="", width=400, height=300, fg_color="black", corner_radius=10)
        self.lbl_cam.pack(pady=(30, 20))
        
        control_frame = ctk.CTkFrame(self.tab_cc, fg_color="transparent")
        control_frame.pack(pady=10)

        self.cb_loai = ctk.CTkComboBox(control_frame, values=["Vào Ca", "Ra Ca"], font=("Arial", 16), height=45, corner_radius=10)
        self.cb_loai.grid(row=0, column=0, padx=15)
        self.cb_ca = ctk.CTkComboBox(control_frame, values=["1", "2", "3"], font=("Arial", 16), height=45, corner_radius=10)
        self.cb_ca.grid(row=0, column=1, padx=15)
        
        self.btn_cam = ctk.CTkButton(self.tab_cc, text="MỞ CAMERA FACE ID", font=("Arial", 18, "bold"), height=60, corner_radius=15, command=self.toggle_cam)
        self.btn_cam.pack(pady=30)

    def toggle_cam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.btn_cam.configure(text="ĐÓNG CAMERA", fg_color="#D32F2F", hover_color="#B71C1C")
            self.is_processing_face = False
            self.scan()
        else:
            self.cap.release()
            self.cap = None
            self.lbl_cam.configure(image="")
            self.btn_cam.configure(text="MỞ CAMERA FACE ID", fg_color=["#3a7ebf", "#1f538d"], hover_color=["#325882", "#14375e"])

    def scan(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                ctk_img = ctk.CTkImage(img, size=(400, 300))
                self.lbl_cam.configure(image=ctk_img)
                
                if not self.is_processing_face:
                    if check_liveness(frame):
                        self.is_processing_face = True
                        threading.Thread(target=self.process_face_recognition, args=(frame.copy(),)).start()

            self.after(20, self.scan)

    def process_face_recognition(self, frame):
        db_faces = lay_tat_ca_khuon_mat()
        ma_nv_matched = None
        for row in db_faces:
            if compare_faces(row.FaceVector, frame):
                ma_nv_matched = row.MaNV
                break
        
        if ma_nv_matched:
            self.after(0, self.show_confirm_ui, ma_nv_matched, frame)
        else:
            self.after(0, self.reset_processing)

    def show_confirm_ui(self, ma_nv, frame):
        if self.cap:
            self.cap.release()
            self.cap = None

        loai_cc = self.cb_loai.get()
        ca_lam = self.cb_ca.get()

        for widget in self.tab_cc.winfo_children():
            widget.destroy()

        nv_info = None
        for nv in lay_danh_sach_nhan_vien():
            if nv.MaNV == ma_nv:
                nv_info = nv
                break

        if not nv_info:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin nhân viên!")
            self.build_live_ui()
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb_frame)
        
        img_pil = Image.fromarray(rgb_frame)
        width, height = img_pil.size
        
        if locations:
            top, right, bottom, left = locations[0]
            # Tính toán phần cắt: lớn hơn khung hình 1-2 cm (~ 40 pixel)
            margin = 40 
            crop_left = max(0, left - margin)
            crop_top = max(0, top - margin)
            crop_right = min(width, right + margin)
            crop_bottom = min(height, bottom + margin)
            # Cắt ảnh
            img_cropped = img_pil.crop((crop_left, crop_top, crop_right, crop_bottom))
            
            draw = ImageDraw.Draw(img_cropped)
            # Vẽ hình vuông xanh lá lên ảnh đã cắt (tọa độ tương đối so với phần cắt)
            new_top = top - crop_top
            new_left = left - crop_left
            new_bottom = bottom - crop_top
            new_right = right - crop_left
            draw.rectangle(((new_left, new_top), (new_right, new_bottom)), outline="#00FF00", width=5)
            
            c_width, c_height = img_cropped.size
            # Tính toán kích thước hiển thị (giữ tỷ lệ)
            display_width = 450
            display_height = int(display_width * c_height / c_width)
            ctk_img = ctk.CTkImage(img_cropped, size=(display_width, display_height))
        else:
            ctk_img = ctk.CTkImage(img_pil, size=(400, 300))

        main_frame = ctk.CTkFrame(self.tab_cc, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        img_frame = ctk.CTkFrame(main_frame, fg_color="#F0F2F5", corner_radius=20, border_width=1, border_color="#E0E5E9")
        img_frame.pack(side="left", padx=20, pady=20)

        lbl_img = ctk.CTkLabel(img_frame, text="", image=ctk_img, corner_radius=10)
        lbl_img.pack(padx=20, pady=20)

        right_frame = ctk.CTkFrame(main_frame, fg_color="#F0F2F5", corner_radius=20, border_width=1, border_color="#E0E5E9")
        right_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(right_frame, text="XÁC NHẬN CHẤM CÔNG", font=("Arial", 30, "bold"), text_color="#1976D2").pack(pady=(30, 20))
        
        # Nhóm thông tin nhân viên
        info_frame = ctk.CTkFrame(right_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#D1D9E6")
        info_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(info_frame, text=f"Mã NV: {nv_info.MaNV}", font=("Arial", 20, "bold"), text_color="#333333").pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(info_frame, text=f"Tên NV: {nv_info.TenNV}", font=("Arial", 20), text_color="#333333").pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(info_frame, text=f"Vai Trò: {nv_info.VaiTro}", font=("Arial", 20), text_color="#333333").pack(anchor="w", padx=20, pady=5)
        
        sdt_str = '0' + str(nv_info.SoDienThoai) if not str(nv_info.SoDienThoai).startswith('0') else str(nv_info.SoDienThoai)
        ctk.CTkLabel(info_frame, text=f"SĐT: {sdt_str}", font=("Arial", 20), text_color="#333333").pack(anchor="w", padx=20, pady=(5, 15))

        # Nhóm thông tin kiểm tra
        check_frame = ctk.CTkFrame(right_frame, fg_color="#FFF8E1", corner_radius=15, border_width=1, border_color="#FFE082")
        check_frame.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(check_frame, text=f"Loại: {loai_cc}   |   Ca: {ca_lam}", font=("Arial", 22, "bold"), text_color="#FF8F00").pack(pady=15)

        def confirm_action():
            try:
                if loai_cc == "Vào Ca":
                    cham_cong_vao(nv_info.MaNV, int(ca_lam))
                else:
                    cham_cong_ra(nv_info.MaNV, int(ca_lam))
                messagebox.showinfo("Thành công", f"Ghi nhận {loai_cc} thành công cho {nv_info.TenNV}!")
                if hasattr(self, 'history_table'): self.load_lich_su()
            except Exception as e:
                messagebox.showerror("Lỗi", "Lỗi CSDL khi chấm công!")
            finally:
                self.build_live_ui()

        def cancel_action():
            self.build_live_ui()

        btn_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        btn_frame.pack(pady=30)

        ctk.CTkButton(btn_frame, text="XÁC NHẬN CHẤM CÔNG", font=("Arial", 18, "bold"), height=60, width=280, corner_radius=15, fg_color="#2E7D32", hover_color="#1B5E20", command=confirm_action).pack(side="left", padx=20)
        ctk.CTkButton(btn_frame, text="HỦY", font=("Arial", 18, "bold"), height=60, width=150, corner_radius=15, fg_color="#D32F2F", hover_color="#B71C1C", command=cancel_action).pack(side="left", padx=20)

    def reset_processing(self):
        self.is_processing_face = False

    def setup_quan_ly_tab(self):
        tab = self.tabview.add("Quản Lý Nhân Viên")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Thêm Nhân Viên Mới", font=("Arial", 16, "bold"), height=45, corner_radius=10, command=self.open_add_nv_popup).pack(side="left")

        # Cập nhật style cho Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        self.tree = ttk.Treeview(tab, columns=("ID", "Ten", "VT", "SDT"), show="headings")
        self.tree.heading("ID", text="Mã NV")
        self.tree.heading("Ten", text="Tên Nhân Viên")
        self.tree.heading("VT", text="Vai Trò")
        self.tree.heading("SDT", text="SĐT")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Ten", width=300)
        self.tree.column("VT", width=200)
        self.tree.column("SDT", width=200)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.open_edit_nv_popup)
        
        self.load_nv()

    def load_nv(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        for n in lay_danh_sach_nhan_vien():
            if n.TrangThai == 1:
                sdt_str = '0' + str(n.SoDienThoai) if not str(n.SoDienThoai).startswith('0') else str(n.SoDienThoai)
                self.tree.insert("", "end", values=(n.MaNV, n.TenNV, n.VaiTro, sdt_str))

    def setup_lich_su_tab(self):
        tab = self.tabview.add("Lịch Sử Chấm Công")
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Làm Mới Dữ Liệu", font=("Arial", 16, "bold"), height=45, corner_radius=10, command=self.load_lich_su).pack(side="left")

        cols = ("ID", "Ten", "Ca", "Ngay", "Vao", "Ra")
        self.history_table = ttk.Treeview(tab, columns=cols, show="headings")
        self.history_table.heading("ID", text="Mã NV")
        self.history_table.heading("Ten", text="Tên Nhân Viên")
        self.history_table.heading("Ca", text="Ca Làm")
        self.history_table.heading("Ngay", text="Ngày Làm")
        self.history_table.heading("Vao", text="Giờ Vào")
        self.history_table.heading("Ra", text="Giờ Ra")
        
        self.history_table.column("ID", width=80, anchor="center")
        self.history_table.column("Ten", width=250)
        self.history_table.column("Ca", width=80, anchor="center")
        self.history_table.column("Ngay", width=150, anchor="center")
        self.history_table.column("Vao", width=120, anchor="center")
        self.history_table.column("Ra", width=120, anchor="center")
        
        self.history_table.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_lich_su()

    def load_lich_su(self):
        for r in self.history_table.get_children(): self.history_table.delete(r)
        for row in lay_lich_su_cham_cong():
            gio_vao = row[4].strftime("%H:%M:%S") if row[4] else "--:--:--"
            gio_ra = row[5].strftime("%H:%M:%S") if row[5] else "--:--:--"
            self.history_table.insert("", "end", values=(row[0], row[1], row[2], row[3].strftime("%Y-%m-%d"), gio_vao, gio_ra))

    def open_add_nv_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Thêm Nhân Viên Mới")
        popup.geometry("650x700")
        popup.corner_radius = 20
        popup.grab_set()

        self.temp_face_vector = None

        main_popup_frame = ctk.CTkFrame(popup, fg_color="transparent")
        main_popup_frame.pack(expand=True, fill="both", padx=30, pady=30)

        ctk.CTkLabel(main_popup_frame, text="Thêm Nhân Viên Mới", font=("Arial", 28, "bold")).pack(pady=(10, 30))

        ctk.CTkLabel(main_popup_frame, text="Tên Nhân Viên:", font=("Arial", 16)).pack(pady=5)
        e_ten = ctk.CTkEntry(main_popup_frame, width=300, font=("Arial", 16), height=40, corner_radius=10)
        e_ten.pack(pady=5)

        ctk.CTkLabel(main_popup_frame, text="Số Điện Thoại:", font=("Arial", 16)).pack(pady=5)
        e_sdt = ctk.CTkEntry(main_popup_frame, width=300, font=("Arial", 16), height=40, corner_radius=10)
        e_sdt.pack(pady=5)

        ctk.CTkLabel(main_popup_frame, text="Mật khẩu:", font=("Arial", 16)).pack(pady=5)
        e_mk = ctk.CTkEntry(main_popup_frame, width=300, font=("Arial", 16), height=40, corner_radius=10, show="*")
        e_mk.pack(pady=5)

        ctk.CTkLabel(main_popup_frame, text="Vai Trò:", font=("Arial", 16)).pack(pady=5)
        c_vt = ctk.CTkComboBox(main_popup_frame, values=["ThuNgan", "NhanVienKho", "NhanVienPhucVu", "QuanLy"], width=300, font=("Arial", 16), height=40, corner_radius=10)
        c_vt.pack(pady=5)

        lbl_face_status = ctk.CTkLabel(main_popup_frame, text="Chưa lấy dữ liệu khuôn mặt", font=("Arial", 16), text_color="#D32F2F")
        lbl_face_status.pack(pady=20)

        def capture_face():
            temp_cap = cv2.VideoCapture(0)
            ret, frame = temp_cap.read()
            temp_cap.release()
            if ret:
                vector = get_face_embedding(frame)
                if vector:
                    self.temp_face_vector = vector
                    lbl_face_status.configure(text="Đã lưu dữ liệu khuôn mặt thành công!", text_color="#2E7D32")
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy khuôn mặt trong camera!")
            else:
                messagebox.showerror("Lỗi", "Lỗi Camera!")

        ctk.CTkButton(main_popup_frame, text="Chụp Dữ Liệu Khuôn Mặt", font=("Arial", 16, "bold"), height=50, corner_radius=12, command=capture_face, fg_color="#F57C00", hover_color="#E65100").pack(pady=10)

        def save():
            try:
                them_nhan_vien(e_ten.get(), c_vt.get(), e_sdt.get(), e_mk.get(), self.temp_face_vector)
                self.load_nv()
                popup.destroy()
                messagebox.showinfo("Thành công", "Đã thêm nhân viên!")
            except:
                messagebox.showerror("Lỗi", "Kiểm tra lại thông tin!")

        ctk.CTkButton(main_popup_frame, text="Lưu Thông Tin", font=("Arial", 18, "bold"), height=60, width=200, corner_radius=15, command=save).pack(pady=40)

    def open_edit_nv_popup(self, e):
        selected = self.tree.selection()
        if not selected: return
        item = self.tree.item(selected[0])['values']

        popup = ctk.CTkToplevel(self)
        popup.title("Cập Nhật Nhân Viên")
        popup.geometry("850x550")
        popup.corner_radius = 20
        popup.grab_set()
        
        self.temp_face_vector = None

        main_popup_frame = ctk.CTkFrame(popup, fg_color="transparent")
        main_popup_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        ctk.CTkLabel(main_popup_frame, text="Cập Nhật Nhân Viên", font=("Arial", 28, "bold")).pack(pady=(10, 30))

        left_frame = ctk.CTkFrame(main_popup_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=20)

        right_frame = ctk.CTkFrame(main_popup_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=20)

        ctk.CTkLabel(left_frame, text="Mã NV:", font=("Arial", 16)).pack(pady=(10, 5))
        e_id = ctk.CTkEntry(left_frame, width=300, font=("Arial", 16), height=40, corner_radius=10)
        e_id.insert(0, item[0])
        e_id.configure(state="readonly")
        e_id.pack(pady=5)

        ctk.CTkLabel(left_frame, text="Tên Nhân Viên:", font=("Arial", 16)).pack(pady=5)
        e_ten = ctk.CTkEntry(left_frame, width=300, font=("Arial", 16), height=40, corner_radius=10)
        e_ten.insert(0, item[1])
        e_ten.pack(pady=5)

        ctk.CTkLabel(left_frame, text="Số Điện Thoại:", font=("Arial", 16)).pack(pady=5)
        e_sdt = ctk.CTkEntry(left_frame, width=300, font=("Arial", 16), height=40, corner_radius=10)
        e_sdt.insert(0, str(item[3]))
        e_sdt.pack(pady=5)

        ctk.CTkLabel(left_frame, text="Mật khẩu (bỏ trống nếu không đổi):", font=("Arial", 16)).pack(pady=5)
        e_mk = ctk.CTkEntry(left_frame, width=300, font=("Arial", 16), height=40, corner_radius=10, show="*")
        e_mk.pack(pady=5)

        ctk.CTkLabel(left_frame, text="Vai Trò:", font=("Arial", 16)).pack(pady=5)
        c_vt = ctk.CTkComboBox(left_frame, values=["ThuNgan", "NhanVienKho", "NhanVienPhucVu", "QuanLy"], width=300, font=("Arial", 16), height=40, corner_radius=10)
        c_vt.set(item[2])
        c_vt.pack(pady=5)

        lbl_face_status = ctk.CTkLabel(right_frame, text="Giữ nguyên khuôn mặt cũ", font=("Arial", 18), text_color="#FF8F00")
        lbl_face_status.pack(pady=30)

        def capture_face():
            temp_cap = cv2.VideoCapture(0)
            ret, frame = temp_cap.read()
            temp_cap.release()
            if ret:
                vector = get_face_embedding(frame)
                if vector:
                    self.temp_face_vector = vector
                    lbl_face_status.configure(text="Đã cập nhật khuôn mặt mới!", text_color="#2E7D32")
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy khuôn mặt trong camera!")
            else:
                messagebox.showerror("Lỗi", "Lỗi Camera!")

        ctk.CTkButton(right_frame, text="Chụp Lại Dữ Liệu Khuôn Mặt", font=("Arial", 16, "bold"), height=50, corner_radius=12, fg_color="#F57C00", hover_color="#E65100", command=capture_face).pack(pady=20)

        def update():
            try:
                sua_nhan_vien(int(e_id.get()), e_ten.get(), c_vt.get(), e_sdt.get(), e_mk.get(), self.temp_face_vector)
                self.load_nv()
                popup.destroy()
                messagebox.showinfo("Thành công", "Đã cập nhật nhân viên!")
            except:
                messagebox.showerror("Lỗi", "Kiểm tra lại thông tin!")

        def delete():
            if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?"):
                xoa_nhan_vien(int(e_id.get()))
                self.load_nv()
                popup.destroy()

        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.pack(pady=40)
        
        ctk.CTkButton(btn_frame, text="Cập Nhật", font=("Arial", 16, "bold"), height=45, corner_radius=10, fg_color="#1976D2", hover_color="#1565C0", command=update, width=120).pack(side="left", padx=15)
        ctk.CTkButton(btn_frame, text="Xóa", font=("Arial", 16, "bold"), height=45, corner_radius=10, fg_color="#D32F2F", hover_color="#B71C1C", command=delete, width=120).pack(side="left", padx=15)