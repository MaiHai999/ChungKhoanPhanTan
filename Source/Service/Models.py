from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class NHANVIEN(Base):
    __tablename__ = 'NHANVIEN'

    ID = Column(Integer, primary_key=True)
    HO = Column(String(30))
    TEN = Column(String(30))
    NGAYSINH = Column(DateTime)
    DIACHI = Column(String(100))
    GIOITINH = Column(String(10))
    SDT = Column(String(10))
    IDCONGTY = Column(String(10))
    DANGHIVIEC = Column(Integer)


class CONGTYCK(Base):
    __tablename__ = 'CONGTYCK'

    ID = Column(String, primary_key=True)
    TENCONGTY = Column(String)

class CTDANHMUC(Base):
    __tablename__ = 'CTDANHMUC'

    IDSAN = Column(String(15), primary_key=True)
    IDQUYDINH = Column(Integer, primary_key=True)
    GIATRI = Column(Float)
    NGAY = Column(DateTime)
    ID = Column(Integer, primary_key=True, autoincrement=True)

class COPHIEU(Base):
    __tablename__ = 'COPHIEU'

    MACP = Column(String(6), primary_key=True)
    TENCONGTY = Column(String(100))
    DIACHI = Column(String(100))
    SDT = Column(String(10))
    FAX = Column(String(100))
    EMAIL = Column(String(100))
    TONGSOLUONGCP = Column(Integer)
    IDSAN = Column(String(15))

    # Quan hệ
    prices = relationship("LICHSUGIA", back_populates="stock")

class LICHSUGIA(Base):
    __tablename__ = 'LICHSUGIA'
    NGAY = Column(DateTime)
    GIASAN = Column(Float)
    GIATRAN = Column(Float)
    GIATHAMCHIEU = Column(Float)
    ID = Column(Integer, primary_key=True)
    IDCOPHIEU = Column(String(6), ForeignKey('COPHIEU.MACP'))

    # Quan hệ
    stock = relationship("COPHIEU", back_populates="prices")


class LENHDAT(Base):
    __tablename__ = 'LENHDAT'

    MATKNH = Column(String(15), primary_key=True)
    MACP = Column(String(6), primary_key=True)
    LOAILENH = Column(String(15))
    LOAIGD = Column(String(15))
    SOLUONG = Column(Integer)
    TRANGTHAI = Column(String(20))
    NGAYDATLENH = Column(DateTime)
    GIA = Column(Float)
    ID = Column(Integer, primary_key=True, autoincrement=True)

class LENHKHOP(Base):
    __tablename__ = 'LENHKHOP'

    IDLENHMUA = Column(Integer, primary_key=True)
    IDLENHBAN = Column(Integer, primary_key=True)
    NGAYKHOP = Column(DateTime)
    SOLUONGKHOP = Column(Integer)
    GIAKHOP = Column(Float)
    PHI = Column(Float)

class NDT(Base):
    __tablename__ = 'NDT'

    MATK = Column(Integer, primary_key=True, autoincrement=True)
    HO = Column(String(30))
    TEN = Column(String(30))
    NGAYSINH = Column(DateTime)
    NOISINH = Column(String(100))
    GIOITINH = Column(String(50))
    DIACHI = Column(String(100))
    EMAIL = Column(String(100))
    CMND = Column(String(20), nullable=False)
    NGAYCAP = Column(DateTime)
    MATKHAU = Column(String(50))
    IDCONGTY = Column(String(10))
    MATKHAUDATLENH = Column(String(20))


class NGANHANG(Base):
    __tablename__ = 'NGANHANG'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    TENNGANHANG = Column(String(100))

    #Quan hệ
    accounts = relationship("TAIKHOANNGANHANG", back_populates="banks")


class TAIKHOANNGANHANG(Base):
    __tablename__ = 'TAIKHOANNGANHANG'

    MATK = Column(String(15), primary_key=True)
    TENTAIKHOAN = Column(String(30))
    IDNDT = Column(Integer)
    IDNGANHANG = Column(Integer, ForeignKey('NGANHANG.ID'))
    SODU = Column(Float)

    #Quan hệ
    banks = relationship("NGANHANG", back_populates="accounts")

class NHANVIENSAN(Base):
    __tablename__ = 'NHANVIENSAN'

    ID = Column(Integer, primary_key=True, autoincrement=True)  # ID nhân viên sàn
    HO = Column(String(30))  # Họ
    TEN = Column(String(30))  # Tên
    NGAYSINH = Column(DateTime)  # Ngày sinh
    DIACHI = Column(String(100))  # Địa chỉ
    GIOITINH = Column(String(10))  # Giới tính
    SDT = Column(String(10))  # Số điện thoại
    IDSAN = Column(String(15), ForeignKey('SANGIAODICH.ID'))

class SANGIAODICH(Base):
    __tablename__ = 'SANGIAODICH'

    ID = Column(String(15), primary_key=True)  # ID sàn giao dịch
    TENSAN = Column(String(70))  # Tên sàn giao dịch

class SOHUUCOPHIEU(Base):
    __tablename__ = 'SOHUUCOPHIEU'

    MACP = Column(String(6), primary_key=True)
    MANDT = Column(Integer, primary_key=True)
    SOLUONG = Column(Integer)


class THAYDOIGIADANHMUC(Base):
    __tablename__ = 'THAYDOIGIADANHMUC'

    IDNHANVIEN = Column(Integer, primary_key=True)
    IDCTDANHMUC = Column(Integer, primary_key=True)

class DANHMUCQUYDINH(Base):
    __tablename__ = 'DANHMUCQUYDINH'

    ID = Column(Integer, primary_key=True, autoincrement=True)  # ID tự động tăng
    TENQUYDINH = Column(String(50))  # Tên quy định