
DROP PROCEDURE IF EXISTS sp_DangNhap;
DROP PROCEDURE IF EXISTS sp_TimKhachHang;
DROP PROCEDURE IF EXISTS sp_LayDanhSachMonAn;
DROP PROCEDURE IF EXISTS sp_LapHoaDon;
DROP PROCEDURE IF EXISTS sp_ThemChiTietHoaDon;
DROP PROCEDURE IF EXISTS sp_TichDiemKhachHang;
DROP PROCEDURE IF EXISTS sp_LapPhieuNhapKho;
DROP PROCEDURE IF EXISTS sp_ThemChiTietNhapKho;
DROP PROCEDURE IF EXISTS sp_ChamCongVao;
DROP PROCEDURE IF EXISTS sp_ChamCongRa;
DROP PROCEDURE IF EXISTS sp_DangKyKhachHang;
DROP PROCEDURE IF EXISTS sp_DoiDiemKhachHang;
DROP PROCEDURE IF EXISTS sp_LayKhuyenMaiHopLe;
DROP PROCEDURE IF EXISTS sp_ThemKhuyenMai;
DROP PROCEDURE IF EXISTS sp_XemChiTietHoaDon;
DROP PROCEDURE IF EXISTS sp_KiemKeKho;
DROP PROCEDURE IF EXISTS sp_LayDanhSachNhanVien;
GO

DROP TABLE IF EXISTS ChiTietNhapKho;
DROP TABLE IF EXISTS PhieuNhapKho;
DROP TABLE IF EXISTS NguyenLieu;
DROP TABLE IF EXISTS NhaCungCap;
DROP TABLE IF EXISTS ChiTietHoaDon;
DROP TABLE IF EXISTS HoaDon;
DROP TABLE IF EXISTS MonAn;
DROP TABLE IF EXISTS ChamCong;
DROP TABLE IF EXISTS CaLamViec;
DROP TABLE IF EXISTS NhanVien;
DROP TABLE IF EXISTS KhuyenMai;
DROP TABLE IF EXISTS KhachHang;
GO
CREATE TABLE KhachHang (
    MaKH INT IDENTITY(1,1) PRIMARY KEY,
    TenKH NVARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15) UNIQUE NOT NULL,
    DiemTichLuy INT DEFAULT 0,
    NgayDangKy DATE DEFAULT GETDATE()
);

CREATE TABLE KhuyenMai (
    MaKM INT IDENTITY(1,1) PRIMARY KEY,
    TenKM NVARCHAR(100) NOT NULL,
    HinhThuc NVARCHAR(50) NOT NULL,
    MucGiam DECIMAL(18,2) NOT NULL,
    DieuKien DECIMAL(18,2) DEFAULT 0,
    NgayBatDau DATE NOT NULL,
    NgayKetThuc DATE NOT NULL
);

CREATE TABLE NhanVien (
    MaNV INT IDENTITY(1,1) PRIMARY KEY,
    TenNV NVARCHAR(100) NOT NULL,
    VaiTro NVARCHAR(50) NOT NULL,
    SoDienThoai VARCHAR(15) UNIQUE NOT NULL,
    MatKhau VARCHAR(255) NOT NULL,
    TrangThai BIT DEFAULT 1,
    FaceVector NVARCHAR(MAX)
);

CREATE TABLE CaLamViec (
    MaCa INT IDENTITY(1,1) PRIMARY KEY,
    TenCa NVARCHAR(50) NOT NULL,
    GioBatDau TIME NOT NULL,
    GioKetThuc TIME NOT NULL
);

CREATE TABLE ChamCong (
    MaCC INT IDENTITY(1,1) PRIMARY KEY,
    MaNV INT NOT NULL,
    MaCa INT NOT NULL,
    NgayLam DATE NOT NULL,
    GioVao TIME,
    GioRa TIME,
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    FOREIGN KEY (MaCa) REFERENCES CaLamViec(MaCa)
);

CREATE TABLE MonAn (
    MaMon INT IDENTITY(1,1) PRIMARY KEY,
    TenMon NVARCHAR(100) NOT NULL,
    GiaBan DECIMAL(18,2) NOT NULL,
    TrangThai BIT DEFAULT 1
);

CREATE TABLE HoaDon (
    MaHD INT IDENTITY(1,1) PRIMARY KEY,
    MaNV INT NOT NULL,
    MaKH INT NULL,
    MaKM INT NULL,
    NgayLap DATETIME DEFAULT GETDATE(),
    TongTien DECIMAL(18,2) NOT NULL,
    TienGiam DECIMAL(18,2) DEFAULT 0,
    ThanhTien DECIMAL(18,2) NOT NULL,
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
    FOREIGN KEY (MaKM) REFERENCES KhuyenMai(MaKM)
);

CREATE TABLE ChiTietHoaDon (
    MaHD INT NOT NULL,
    MaMon INT NOT NULL,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(18,2) NOT NULL,
    ThanhTien DECIMAL(18,2) NOT NULL,
    PRIMARY KEY (MaHD, MaMon),
    FOREIGN KEY (MaHD) REFERENCES HoaDon(MaHD),
    FOREIGN KEY (MaMon) REFERENCES MonAn(MaMon)
);

CREATE TABLE NhaCungCap (
    MaNCC INT IDENTITY(1,1) PRIMARY KEY,
    TenNCC NVARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(15) NOT NULL,
    DiaChi NVARCHAR(255)
);

CREATE TABLE NguyenLieu (
    MaNL INT IDENTITY(1,1) PRIMARY KEY,
    TenNL NVARCHAR(100) NOT NULL,
    DonViTinh NVARCHAR(20) NOT NULL,
    SoLuongTon INT DEFAULT 0
);

CREATE TABLE PhieuNhapKho (
    MaPN INT IDENTITY(1,1) PRIMARY KEY,
    MaNV INT NOT NULL,
    MaNCC INT NOT NULL,
    NgayNhap DATETIME DEFAULT GETDATE(),
    TongTien DECIMAL(18,2) NOT NULL,
    TrangThai NVARCHAR(50) DEFAULT 'DaDuyet',
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    FOREIGN KEY (MaNCC) REFERENCES NhaCungCap(MaNCC)
);

CREATE TABLE ChiTietNhapKho (
    MaPN INT NOT NULL,
    MaNL INT NOT NULL,
    SoLuong INT NOT NULL,
    DonGia DECIMAL(18,2) NOT NULL,
    ThanhTien DECIMAL(18,2) NOT NULL,
    PRIMARY KEY (MaPN, MaNL),
    FOREIGN KEY (MaPN) REFERENCES PhieuNhapKho(MaPN),
    FOREIGN KEY (MaNL) REFERENCES NguyenLieu(MaNL)
);
GO

CREATE PROCEDURE sp_DangNhap
    @SoDienThoai VARCHAR(15),
    @MatKhau VARCHAR(255)
AS
BEGIN
    SELECT MaNV, TenNV, VaiTro, TrangThai
    FROM NhanVien
    WHERE SoDienThoai = @SoDienThoai AND MatKhau = @MatKhau;
END;
GO

CREATE PROCEDURE sp_TimKhachHang
    @SoDienThoai VARCHAR(15)
AS
BEGIN
    SELECT MaKH, TenKH, DiemTichLuy
    FROM KhachHang
    WHERE SoDienThoai = @SoDienThoai;
END;
GO

CREATE PROCEDURE sp_LayDanhSachMonAn
AS
BEGIN
    SELECT MaMon, TenMon, GiaBan 
    FROM MonAn 
    WHERE TrangThai = 1;
END;
GO

CREATE PROCEDURE sp_LapHoaDon
    @MaNV INT,
    @MaKH INT,
    @MaKM INT,
    @TongTien DECIMAL(18,2),
    @TienGiam DECIMAL(18,2),
    @ThanhTien DECIMAL(18,2)
AS
BEGIN
    INSERT INTO HoaDon (MaNV, MaKH, MaKM, TongTien, TienGiam, ThanhTien)
    VALUES (@MaNV, @MaKH, @MaKM, @TongTien, @TienGiam, @ThanhTien);
    SELECT SCOPE_IDENTITY() AS MaHDMoi;
END;
GO

CREATE PROCEDURE sp_ThemChiTietHoaDon
    @MaHD INT,
    @MaMon INT,
    @SoLuong INT,
    @DonGia DECIMAL(18,2)
AS
BEGIN
    DECLARE @ThanhTien DECIMAL(18,2) = @SoLuong * @DonGia;
    INSERT INTO ChiTietHoaDon (MaHD, MaMon, SoLuong, DonGia, ThanhTien)
    VALUES (@MaHD, @MaMon, @SoLuong, @DonGia, @ThanhTien);
END;
GO

CREATE PROCEDURE sp_TichDiemKhachHang
    @MaKH INT,
    @DiemCong INT
AS
BEGIN
    UPDATE KhachHang
    SET DiemTichLuy = DiemTichLuy + @DiemCong
    WHERE MaKH = @MaKH;
END;
GO

CREATE PROCEDURE sp_LapPhieuNhapKho
    @MaNV INT,
    @MaNCC INT,
    @TongTien DECIMAL(18,2)
AS
BEGIN
    INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai)
    VALUES (@MaNV, @MaNCC, @TongTien, 'DaDuyet');
    SELECT SCOPE_IDENTITY() AS MaPNMoi;
END;
GO

CREATE PROCEDURE sp_ThemChiTietNhapKho
    @MaPN INT,
    @MaNL INT,
    @SoLuong INT,
    @DonGia DECIMAL(18,2)
AS
BEGIN
    DECLARE @ThanhTien DECIMAL(18,2) = @SoLuong * @DonGia;
    
    INSERT INTO ChiTietNhapKho (MaPN, MaNL, SoLuong, DonGia, ThanhTien)
    VALUES (@MaPN, @MaNL, @SoLuong, @DonGia, @ThanhTien);
    
    UPDATE NguyenLieu
    SET SoLuongTon = SoLuongTon + @SoLuong
    WHERE MaNL = @MaNL;
END;
GO

CREATE PROCEDURE sp_ChamCongVao
    @MaNV INT,
    @MaCa INT
AS
BEGIN
    INSERT INTO ChamCong (MaNV, MaCa, NgayLam, GioVao)
    VALUES (@MaNV, @MaCa, CAST(GETDATE() AS DATE), CAST(GETDATE() AS TIME));
END;
GO

CREATE PROCEDURE sp_ChamCongRa
    @MaNV INT,
    @MaCa INT
AS
BEGIN
    UPDATE ChamCong
    SET GioRa = CAST(GETDATE() AS TIME)
    WHERE MaNV = @MaNV AND MaCa = @MaCa AND NgayLam = CAST(GETDATE() AS DATE);
END;
GO

CREATE PROCEDURE sp_DangKyKhachHang
    @TenKH NVARCHAR(100),
    @SoDienThoai VARCHAR(15)
AS
BEGIN
    INSERT INTO KhachHang (TenKH, SoDienThoai, DiemTichLuy, NgayDangKy)
    VALUES (@TenKH, @SoDienThoai, 0, GETDATE());
    
    SELECT SCOPE_IDENTITY() AS MaKHMoi;
END;
GO

CREATE PROCEDURE sp_DoiDiemKhachHang
    @MaKH INT,
    @DiemTru INT
AS
BEGIN
    UPDATE KhachHang
    SET DiemTichLuy = DiemTichLuy - @DiemTru
    WHERE MaKH = @MaKH AND DiemTichLuy >= @DiemTru;
END;
GO

CREATE PROCEDURE sp_LayKhuyenMaiHopLe
    @TongTien DECIMAL(18,2)
AS
BEGIN
    SELECT MaKM, TenKM, HinhThuc, MucGiam, DieuKien
    FROM KhuyenMai
    WHERE CAST(GETDATE() AS DATE) BETWEEN NgayBatDau AND NgayKetThuc
    AND @TongTien >= DieuKien;
END;
GO

CREATE PROCEDURE sp_ThemKhuyenMai
    @TenKM NVARCHAR(100),
    @HinhThuc NVARCHAR(50),
    @MucGiam DECIMAL(18,2),
    @DieuKien DECIMAL(18,2),
    @NgayBatDau DATE,
    @NgayKetThuc DATE
AS
BEGIN
    INSERT INTO KhuyenMai (TenKM, HinhThuc, MucGiam, DieuKien, NgayBatDau, NgayKetThuc)
    VALUES (@TenKM, @HinhThuc, @MucGiam, @DieuKien, @NgayBatDau, @NgayKetThuc);
END;
GO

CREATE PROCEDURE sp_XemChiTietHoaDon
    @MaHD INT
AS
BEGIN
    SELECT c.MaMon, m.TenMon, c.SoLuong, c.DonGia, c.ThanhTien
    FROM ChiTietHoaDon c
    JOIN MonAn m ON c.MaMon = m.MaMon
    WHERE c.MaHD = @MaHD;
END;
GO

CREATE PROCEDURE sp_KiemKeKho
AS
BEGIN
    SELECT MaNL, TenNL, DonViTinh, SoLuongTon
    FROM NguyenLieu;
END;
GO

CREATE PROCEDURE sp_LayDanhSachNhanVien
AS
BEGIN
    SELECT MaNV, TenNV, VaiTro, SoDienThoai, TrangThai
    FROM NhanVien;
END;
GO

INSERT INTO NhanVien (TenNV, VaiTro, SoDienThoai, MatKhau, TrangThai) VALUES
(N'Nguyễn Tuyền Ánh Nguyệt', 'QuanLy', '0901234567', '123456', 1),
(N'Nguyễn Đức Thành Phát', 'ThuNgan', '0901234568', '123456', 1),
(N'Nguyễn Văn Bảo', 'NhanVienKho', '0901234569', '123456', 1),
(N'Trần Văn Luân', 'NhanVienPhucVu', '0901234570', '123456', 1),
(N'Lê Hoàng Anh', 'ThuNgan', '0901234571', '123456', 1),
(N'Phạm Thị Mai', 'NhanVienPhucVu', '0901234572', '123456', 1),
(N'Vũ Đức Trí', 'NhanVienKho', '0901234573', '123456', 1),
(N'Đặng Thu Thảo', 'ThuNgan', '0901234574', '123456', 1),
(N'Hoàng Ngọc Sang', 'NhanVienPhucVu', '0901234575', '123456', 1),
(N'Trần Thị Cẩm Tú', 'QuanLy', '0901234576', '123456', 1);
GO

INSERT INTO CaLamViec (TenCa, GioBatDau, GioKetThuc) VALUES
(N'Ca Sáng', '06:00:00', '14:00:00'),
(N'Ca Chiều', '14:00:00', '22:00:00'),
(N'Ca Đêm', '22:00:00', '06:00:00');
GO

INSERT INTO ChamCong (MaNV, MaCa, NgayLam, GioVao, GioRa) VALUES
(1, 1, DATEADD(day, -2, CAST(GETDATE() AS DATE)), '05:55:00', '14:05:00'),
(2, 1, DATEADD(day, -2, CAST(GETDATE() AS DATE)), '05:50:00', '14:02:00'),
(3, 2, DATEADD(day, -2, CAST(GETDATE() AS DATE)), '13:50:00', '22:10:00'),
(4, 2, DATEADD(day, -2, CAST(GETDATE() AS DATE)), '13:55:00', '22:05:00'),
(1, 1, DATEADD(day, -1, CAST(GETDATE() AS DATE)), '05:58:00', '14:01:00'),
(5, 1, DATEADD(day, -1, CAST(GETDATE() AS DATE)), '05:45:00', '14:15:00'),
(6, 2, DATEADD(day, -1, CAST(GETDATE() AS DATE)), '13:40:00', '22:00:00'),
(7, 3, DATEADD(day, -1, CAST(GETDATE() AS DATE)), '21:50:00', '06:05:00'),
(1, 1, CAST(GETDATE() AS DATE), '05:50:00', '14:00:00'),
(2, 1, CAST(GETDATE() AS DATE), '05:52:00', '14:10:00'),
(8, 2, CAST(GETDATE() AS DATE), '13:55:00', '22:15:00'),
(9, 3, CAST(GETDATE() AS DATE), '21:55:00', NULL);
GO

INSERT INTO NhaCungCap (TenNCC, SoDienThoai, DiaChi) VALUES
(N'Công ty Thực phẩm sạch CP', '19001122', N'KCN Tân Bình, TP.HCM'),
(N'Đại lý nước giải khát miền Nam', '19003344', N'Quận 10, TP.HCM'),
(N'Hợp tác xã rau sạch Đà Lạt', '0912345678', N'Lâm Đồng'),
(N'Lò bánh mì Hữu Nghị', '02838123456', N'Tân Phú, TP.HCM'),
(N'Nhà phân phối gia vị Chinsu', '19005566', N'Quận 7, TP.HCM'),
(N'Công ty TNHH Bao bì Vina', '0933445566', N'Bình Tân, TP.HCM'),
(N'Đại lý thịt bò nhập khẩu', '0988112233', N'Quận 3, TP.HCM');
GO

INSERT INTO NguyenLieu (TenNL, DonViTinh, SoLuongTon) VALUES
(N'Thịt gà tươi', N'Kg', 0),
(N'Thịt bò băm', N'Kg', 0),
(N'Khoai tây đông lạnh', N'Kg', 0),
(N'Syrup Coca Cola', N'Lít', 0),
(N'Bánh mì Hamburger', N'Cái', 0),
(N'Rau xà lách', N'Kg', 0),
(N'Dầu ăn Tường An', N'Can 5L', 0),
(N'Sốt Mayonnaise', N'Kg', 0),
(N'Phô mai lát', N'Hộp', 0),
(N'Syrup Sprite', N'Lít', 0),
(N'Ly nhựa loại vừa', N'Cái', 0),
(N'Ly nhựa loại lớn', N'Cái', 0),
(N'Hộp giấy đựng Gà', N'Cái', 0),
(N'Tương ớt chinsu', N'Can 5L', 0),
(N'Cà chua tươi', N'Kg', 0);
GO

INSERT INTO MonAn (TenMon, GiaBan, TrangThai) VALUES
(N'Gà rán giòn cay', 40000, 1),
(N'Gà rán truyền thống', 35000, 1),
(N'Hamburger bò phô mai', 55000, 1),
(N'Khoai tây chiên cỡ vừa', 25000, 1),
(N'Khoai tây chiên phô mai', 35000, 1),
(N'Nước ngọt Coca Cola', 15000, 1),
(N'Combo Gà + Khoai + Nước', 75000, 1),
(N'Hamburger tôm xốt nấm', 65000, 1),
(N'Gà quay tiêu (1/2 con)', 85000, 1),
(N'Mì Ý sốt bò băm', 45000, 1),
(N'Salad cá ngừ', 30000, 1),
(N'Nước ngọt Sprite', 15000, 1),
(N'Trà đào cam sả', 25000, 1),
(N'Trà sữa trân châu', 30000, 1),
(N'Combo 2 người siêu tiết kiệm', 140000, 1),
(N'Combo Gia Đình Tụ Tập', 250000, 1),
(N'Gà popcorn size L', 45000, 1),
(N'Bánh tart trứng (2 cái)', 25000, 1);
GO

INSERT INTO KhuyenMai (TenKM, HinhThuc, MucGiam, DieuKien, NgayBatDau, NgayKetThuc) VALUES
(N'Giảm giá khung giờ vàng', N'PhanTram', 10, 100000, CAST(GETDATE()-5 AS DATE), CAST(GETDATE()+30 AS DATE)),
(N'Voucher tiền mặt 20k', N'TienMat', 20000, 150000, CAST(GETDATE()-2 AS DATE), CAST(GETDATE()+15 AS DATE)),
(N'Siêu sale cuối tuần', N'PhanTram', 15, 200000, CAST(GETDATE()-10 AS DATE), CAST(GETDATE()+20 AS DATE)),
(N'Mừng khai trương cơ sở mới', N'TienMat', 30000, 250000, CAST(GETDATE()-1 AS DATE), CAST(GETDATE()+7 AS DATE)),
(N'Tri ân khách hàng thân thiết', N'PhanTram', 5, 50000, CAST(GETDATE()-30 AS DATE), CAST(GETDATE()+60 AS DATE)),
(N'Voucher giảm sâu 50k', N'TienMat', 50000, 300000, CAST(GETDATE() AS DATE), CAST(GETDATE()+10 AS DATE));
GO

INSERT INTO KhachHang (TenKH, SoDienThoai, DiemTichLuy, NgayDangKy) VALUES
(N'Khách vãng lai', '0000000000', 0, GETDATE()),
(N'Trần Tiểu Vy', '0911223344', 150, DATEADD(day, -30, GETDATE())),
(N'Lê Minh Sơn', '0988776655', 320, DATEADD(day, -25, GETDATE())),
(N'Nguyễn Thu Hà', '0909111222', 45, DATEADD(day, -10, GETDATE())),
(N'Phạm Quang Hùng', '0933444555', 80, DATEADD(day, -5, GETDATE())),
(N'Lê Thị Bích', '0912349876', 200, DATEADD(day, -15, GETDATE())),
(N'Đinh Tuấn Tài', '0987654321', 10, DATEADD(day, -2, GETDATE())),
(N'Vũ Ngọc Anh', '0905123123', 500, DATEADD(day, -60, GETDATE())),
(N'Hoàng Minh Trí', '0938999888', 120, DATEADD(day, -20, GETDATE()));
GO

DECLARE @MaPN1 INT, @MaPN2 INT, @MaPN3 INT, @MaPN4 INT, @MaPN5 INT;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) VALUES (3, 1, 5500000, 'DaDuyet', DATEADD(day, -5, GETDATE()));
SET @MaPN1 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @MaPN1, @MaNL = 1, @SoLuong = 100, @DonGia = 40000;
EXEC sp_ThemChiTietNhapKho @MaPN = @MaPN1, @MaNL = 2, @SoLuong = 10, @DonGia = 150000;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) VALUES (3, 2, 1500000, 'DaDuyet', DATEADD(day, -4, GETDATE()));
SET @MaPN2 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @MaPN2, @MaNL = 4, @SoLuong = 50, @DonGia = 30000;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) VALUES (3, 4, 500000, 'DaDuyet', DATEADD(day, -3, GETDATE()));
SET @MaPN3 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @MaPN3, @MaNL = 5, @SoLuong = 200, @DonGia = 2500;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) VALUES (7, 5, 2000000, 'DaDuyet', DATEADD(day, -2, GETDATE()));
SET @MaPN4 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @MaPN4, @MaNL = 14, @SoLuong = 20, @DonGia = 100000;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) VALUES (7, 6, 1200000, 'DaDuyet', DATEADD(day, -1, GETDATE()));
SET @MaPN5 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @MaPN5, @MaNL = 13, @SoLuong = 500, @DonGia = 2400;
GO

DECLARE @MaHD1 INT, @MaHD2 INT, @MaHD3 INT, @MaHD4 INT, @MaHD5 INT, @MaHD6 INT, @MaHD7 INT, @MaHD8 INT;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (2, 1, NULL, DATEADD(day, -3, GETDATE()), 115000, 0, 115000);
SET @MaHD1 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD1, @MaMon = 1, @SoLuong = 2, @DonGia = 40000;
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD1, @MaMon = 5, @SoLuong = 1, @DonGia = 35000;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (2, 2, 1, DATEADD(day, -3, GETDATE()), 130000, 13000, 117000);
SET @MaHD2 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD2, @MaMon = 7, @SoLuong = 1, @DonGia = 75000;
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD2, @MaMon = 3, @SoLuong = 1, @DonGia = 55000;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (5, 3, 2, DATEADD(day, -2, GETDATE()), 170000, 20000, 150000);
SET @MaHD3 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD3, @MaMon = 2, @SoLuong = 4, @DonGia = 35000;
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD3, @MaMon = 6, @SoLuong = 2, @DonGia = 15000;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (5, 4, NULL, DATEADD(day, -2, GETDATE()), 250000, 0, 250000);
SET @MaHD4 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD4, @MaMon = 16, @SoLuong = 1, @DonGia = 250000;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (8, 5, 3, DATEADD(day, -1, GETDATE()), 225000, 33750, 191250);
SET @MaHD5 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD5, @MaMon = 15, @SoLuong = 1, @DonGia = 140000;
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD5, @MaMon = 9, @SoLuong = 1, @DonGia = 85000;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (8, 6, 2, DATEADD(day, -1, GETDATE()), 180000, 20000, 160000);
SET @MaHD6 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD6, @MaMon = 10, @SoLuong = 2, @DonGia = 45000;
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD6, @MaMon = 17, @SoLuong = 2, @DonGia = 45000;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (2, 8, 4, CAST(GETDATE() AS DATE), 310000, 30000, 280000);
SET @MaHD7 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD7, @MaMon = 16, @SoLuong = 1, @DonGia = 250000;
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD7, @MaMon = 11, @SoLuong = 2, @DonGia = 30000;

INSERT INTO HoaDon (MaNV, MaKH, MaKM, NgayLap, TongTien, TienGiam, ThanhTien) VALUES (2, 1, NULL, CAST(GETDATE() AS DATE), 55000, 0, 55000);
SET @MaHD8 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD8, @MaMon = 18, @SoLuong = 1, @DonGia = 25000;
EXEC sp_ThemChiTietHoaDon @MaHD = @MaHD8, @MaMon = 14, @SoLuong = 1, @DonGia = 30000;
GO
DECLARE @PN_Demo1 INT, @PN_Demo2 INT, @PN_Demo3 INT;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) 
VALUES (3, 3, 800000, 'DaDuyet', GETDATE());
SET @PN_Demo1 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @PN_Demo1, @MaNL = 6, @SoLuong = 20, @DonGia = 25000;
EXEC sp_ThemChiTietNhapKho @MaPN = @PN_Demo1, @MaNL = 15, @SoLuong = 15, @DonGia = 20000;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) 
VALUES (7, 7, 3600000, 'DaDuyet', GETDATE());
SET @PN_Demo2 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @PN_Demo2, @MaNL = 2, @SoLuong = 30, @DonGia = 120000;

INSERT INTO PhieuNhapKho (MaNV, MaNCC, TongTien, TrangThai, NgayNhap) 
VALUES (3, 1, 2100000, 'DaDuyet', GETDATE());
SET @PN_Demo3 = SCOPE_IDENTITY();
EXEC sp_ThemChiTietNhapKho @MaPN = @PN_Demo3, @MaNL = 1, @SoLuong = 50, @DonGia = 42000;

SELECT 
    pn.MaPN AS [Mã Phiếu], 
    nv.TenNV AS [Người Lập], 
    ncc.TenNCC AS [Nhà Cung Cấp], 
    CONVERT(VARCHAR(16), pn.NgayNhap, 120) AS [Ngày Nhập], 
    REPLACE(CONVERT(VARCHAR, CAST(pn.TongTien AS MONEY), 1), '.00', '') + ' VNĐ' AS [Tổng Tiền], 
    pn.TrangThai AS [Trạng Thái]
FROM PhieuNhapKho pn
JOIN NhanVien nv ON pn.MaNV = nv.MaNV
JOIN NhaCungCap ncc ON pn.MaNCC = ncc.MaNCC
ORDER BY pn.MaPN DESC;

SELECT 
    ct.MaPN AS [Mã Phiếu], 
    nl.TenNL AS [Tên Nguyên Liệu], 
    ct.SoLuong AS [Số Lượng], 
    nl.DonViTinh AS [ĐVT], 
    REPLACE(CONVERT(VARCHAR, CAST(ct.DonGia AS MONEY), 1), '.00', '') AS [Đơn Giá], 
    REPLACE(CONVERT(VARCHAR, CAST(ct.ThanhTien AS MONEY), 1), '.00', '') AS [Thành Tiền]
FROM ChiTietNhapKho ct
JOIN NguyenLieu nl ON ct.MaNL = nl.MaNL
ORDER BY ct.MaPN DESC;
SELECT * FROM NhanVien;
SELECT * FROM PhieuNhapKho;