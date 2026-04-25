import pyodbc

_conn = None

def ket_noi_db():
    global _conn
    if _conn is None:
        chuoi_ket_noi = (
            r'DRIVER={ODBC Driver 17 for SQL Server};' 
            r'SERVER=.;'
            r'DATABASE=QLCuaHangThucAnNhanh;'
            r'Trusted_Connection=yes;'
        )
        _conn = pyodbc.connect(chuoi_ket_noi)
    return _conn

def dang_nhap(so_dien_thoai, mat_khau):
    cursor = ket_noi_db().cursor()
    cursor.execute("{CALL sp_DangNhap (?, ?)}", (so_dien_thoai, mat_khau))
    return cursor.fetchone()

def lay_danh_sach_mon_an():
    cursor = ket_noi_db().cursor()
    cursor.execute("{CALL sp_LayDanhSachMonAn}")
    return cursor.fetchall()

def them_mon_an(ten_mon, gia_ban):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO MonAn (TenMon, GiaBan, TrangThai) VALUES (?, ?, 1)", (ten_mon, gia_ban))
    conn.commit()

def sua_mon_an(ma_mon, ten_mon, gia_ban):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE MonAn SET TenMon = ?, GiaBan = ? WHERE MaMon = ?", (ten_mon, gia_ban, ma_mon))
    conn.commit()

def xoa_mon_an(ma_mon):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE MonAn SET TrangThai = 0 WHERE MaMon = ?", (ma_mon,))
    conn.commit()

def lay_danh_sach_nhan_vien():
    cursor = ket_noi_db().cursor()
    cursor.execute("{CALL sp_LayDanhSachNhanVien}")
    return cursor.fetchall()

def them_nhan_vien(ten, vaitro, sdt, matkhau, face_vector):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO NhanVien (TenNV, VaiTro, SoDienThoai, MatKhau, TrangThai, FaceVector) VALUES (?, ?, ?, ?, 1, ?)", (ten, vaitro, sdt, matkhau, face_vector))
    conn.commit()

def sua_nhan_vien(ma_nv, ten, vaitro, sdt, matkhau, face_vector):
    conn = ket_noi_db()
    cursor = conn.cursor()
    if matkhau:
        if face_vector:
            cursor.execute("UPDATE NhanVien SET TenNV = ?, VaiTro = ?, SoDienThoai = ?, MatKhau = ?, FaceVector = ? WHERE MaNV = ?", (ten, vaitro, sdt, matkhau, face_vector, ma_nv))
        else:
            cursor.execute("UPDATE NhanVien SET TenNV = ?, VaiTro = ?, SoDienThoai = ?, MatKhau = ? WHERE MaNV = ?", (ten, vaitro, sdt, matkhau, ma_nv))
    else:
        if face_vector:
            cursor.execute("UPDATE NhanVien SET TenNV = ?, VaiTro = ?, SoDienThoai = ?, FaceVector = ? WHERE MaNV = ?", (ten, vaitro, sdt, face_vector, ma_nv))
        else:
            cursor.execute("UPDATE NhanVien SET TenNV = ?, VaiTro = ?, SoDienThoai = ? WHERE MaNV = ?", (ten, vaitro, sdt, ma_nv))
    conn.commit()

def xoa_nhan_vien(ma_nv):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE NhanVien SET TrangThai = 0 WHERE MaNV = ?", (ma_nv,))
    conn.commit()

def cap_nhat_trang_thai_nhan_vien(ma_nv, trang_thai):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE NhanVien SET TrangThai = ? WHERE MaNV = ?", (trang_thai, ma_nv))
    conn.commit()

def lay_tat_ca_khuon_mat():
    cursor = ket_noi_db().cursor()
    cursor.execute("SELECT MaNV, FaceVector FROM NhanVien WHERE FaceVector IS NOT NULL AND TrangThai = 1")
    return cursor.fetchall()

def cham_cong_vao(ma_nv, ma_ca):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("{CALL sp_ChamCongVao (?, ?)}", (ma_nv, ma_ca))
    conn.commit()

def cham_cong_ra(ma_nv, ma_ca):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("{CALL sp_ChamCongRa (?, ?)}", (ma_nv, ma_ca))
    conn.commit()

def lay_lich_su_cham_cong():
    cursor = ket_noi_db().cursor()
    cursor.execute("""
        SELECT c.MaNV, n.TenNV, c.MaCa, c.NgayLam, c.GioVao, c.GioRa 
        FROM ChamCong c 
        JOIN NhanVien n ON c.MaNV = n.MaNV 
        ORDER BY c.NgayLam DESC, c.GioVao DESC
    """)
    return cursor.fetchall()

def tim_khach_hang(sdt):
    cursor = ket_noi_db().cursor()
    cursor.execute("{CALL sp_TimKhachHang (?)}", (sdt,))
    return cursor.fetchone()

def dang_ky_khach_hang(tenkh, sdt):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("SET NOCOUNT ON; EXEC sp_DangKyKhachHang ?, ?", (tenkh, sdt))
    makh = cursor.fetchone()[0]
    conn.commit()
    return makh

def lay_danh_sach_khach_hang():
    cursor = ket_noi_db().cursor()
    cursor.execute("SELECT MaKH, TenKH, SoDienThoai, DiemTichLuy, NgayDangKy FROM KhachHang")
    return cursor.fetchall()

def kiem_tra_khuyen_mai(tong_tien):
    cursor = ket_noi_db().cursor()
    cursor.execute("{CALL sp_LayKhuyenMaiHopLe (?)}", (tong_tien,))
    return cursor.fetchone()

def them_khuyen_mai(ten, hinhthuc, mucgiam, dieukien, ngaybd, ngaykt):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("{CALL sp_ThemKhuyenMai (?, ?, ?, ?, ?, ?)}", (ten, hinhthuc, mucgiam, dieukien, ngaybd, ngaykt))
    conn.commit()

def lay_tat_ca_khuyen_mai():
    cursor = ket_noi_db().cursor()
    cursor.execute("SELECT * FROM KhuyenMai")
    return cursor.fetchall()

def lap_hoa_don(manv, makh, makm, tongtien, tiengiam, thanhtien):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("SET NOCOUNT ON; EXEC sp_LapHoaDon ?, ?, ?, ?, ?, ?", (manv, makh, makm, tongtien, tiengiam, thanhtien))
    mahd = cursor.fetchone()[0]
    conn.commit()
    return mahd

def them_cthd(mahd, mamon, sl, dongia):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("{CALL sp_ThemChiTietHoaDon (?, ?, ?, ?)}", (mahd, mamon, sl, dongia))
    conn.commit()

def lay_danh_sach_hoa_don():
    cursor = ket_noi_db().cursor()
    cursor.execute("""
        SELECT h.MaHD, h.NgayLap, n.TenNV, ISNULL(k.TenKH, N'Khách vãng lai'), h.ThanhTien 
        FROM HoaDon h
        JOIN NhanVien n ON h.MaNV = n.MaNV
        LEFT JOIN KhachHang k ON h.MaKH = k.MaKH
        ORDER BY h.NgayLap DESC
    """)
    return cursor.fetchall()

def xem_chi_tiet_hoa_don(ma_hd):
    cursor = ket_noi_db().cursor()
    cursor.execute("{CALL sp_XemChiTietHoaDon (?)}", (ma_hd,))
    return cursor.fetchall()

def tich_diem(makh, diem):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("{CALL sp_TichDiemKhachHang (?, ?)}", (makh, diem))
    conn.commit()

def doi_diem_khach_hang(ma_kh, diem_tru):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("{CALL sp_DoiDiemKhachHang (?, ?)}", (ma_kh, diem_tru))
    conn.commit()

def lay_nguyen_lieu():
    cursor = ket_noi_db().cursor()
    cursor.execute("{CALL sp_KiemKeKho}")
    return cursor.fetchall()

def lay_danh_sach_nha_cung_cap():
    cursor = ket_noi_db().cursor()
    cursor.execute("SELECT MaNCC, TenNCC FROM NhaCungCap")
    return cursor.fetchall()

def them_nha_cung_cap(ten_ncc, sdt, dia_chi):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO NhaCungCap (TenNCC, SoDienThoai, DiaChi) VALUES (?, ?, ?)", (ten_ncc, sdt, dia_chi))
    conn.commit()

def lay_tat_ca_nguyen_lieu():
    cursor = ket_noi_db().cursor()
    cursor.execute("SELECT MaNL, TenNL FROM NguyenLieu")
    return cursor.fetchall()

def them_nguyen_lieu(ten_nl, don_vi):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO NguyenLieu (TenNL, DonViTinh, SoLuongTon) VALUES (?, ?, 0)", (ten_nl, don_vi))
    conn.commit()

def lap_phieu_nhap_kho(ma_nv, ma_ncc, tong_tien):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("SET NOCOUNT ON; EXEC sp_LapPhieuNhapKho ?, ?, ?", (ma_nv, ma_ncc, tong_tien))
    ma_pn = cursor.fetchone()[0]
    conn.commit()
    return ma_pn

def them_chi_tiet_nhap_kho(ma_pn, ma_nl, so_luong, don_gia):
    conn = ket_noi_db()
    cursor = conn.cursor()
    cursor.execute("{CALL sp_ThemChiTietNhapKho (?, ?, ?, ?)}", (ma_pn, ma_nl, so_luong, don_gia))
    conn.commit()

def lay_lich_su_nhap_kho():
    cursor = ket_noi_db().cursor()
    cursor.execute("""
        SELECT p.MaPN, p.NgayNhap, n.TenNV, c.TenNCC, p.TongTien, p.TrangThai 
        FROM PhieuNhapKho p 
        JOIN NhanVien n ON p.MaNV = n.MaNV 
        JOIN NhaCungCap c ON p.MaNCC = c.MaNCC 
        ORDER BY p.NgayNhap DESC
    """)
    return cursor.fetchall()

def xem_chi_tiet_phieu_nhap(ma_pn):
    cursor = ket_noi_db().cursor()
    cursor.execute("""
        SELECT c.MaNL, n.TenNL, c.SoLuong, c.DonGia, c.ThanhTien 
        FROM ChiTietNhapKho c 
        JOIN NguyenLieu n ON c.MaNL = n.MaNL 
        WHERE c.MaPN = ?
    """, (ma_pn,))
    return cursor.fetchall()