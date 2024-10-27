from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash
from sqlalchemy.exc import NoResultFound
from flask_jwt_extended import get_jwt_identity


from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort, redirect

from Source.Utiles.CustomResponse import *
from Source.Service.Models import *
from Source.Utiles.HandleExceptions import *
from Source.Utiles.CommonUtiles import *

employee_blueprint = Blueprint('employee', __name__)

@employee_blueprint.route('/add' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def addEmployee():
    identity = get_jwt_identity()
    ho = request.json.get('ho')
    ten = request.json.get('ten')
    ngaySinh = request.json.get('ngaySinh')
    diaChi = request.json.get('diaChi')
    gioiTinh = request.json.get('gioiTinh')
    sdt = request.json.get('sdt')
    daNghiViec = request.json.get('daNghiViec')
    idCongTy = "010" if identity["severName"] == os.environ.get("SEVER_NAME_CONGTY_010") else "020"
    sessionDB = CommonUtiles.getSessionDB(identity)

    nhanVien = NHANVIEN(HO=ho, TEN=ten, NGAYSINH=ngaySinh, DIACHI=diaChi, GIOITINH=gioiTinh, SDT=sdt, IDCONGTY= idCongTy, DANGHIVIEC=daNghiViec)
    CommonUtiles.addCustom(nhanVien, sessionDB)

    try:
        sessionDB.commit()
    except Exception as e:
        sessionDB.rollback()
    finally:
        sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()


@employee_blueprint.route('/delete' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def deleteEmployee():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)
    idnv = request.json.get('IDNV')

    nhanVien = sessionDB.query(NHANVIEN).filter(NHANVIEN.ID == idnv).first()
    sessionDB.delete(nhanVien)

    try:
        sessionDB.commit()
    except Exception as e:
        sessionDB.rollback()
    finally:
        sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()


@employee_blueprint.route('/update' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def updateEmployee():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)
    idnv = request.json.get('IDNV')
    ho = request.json.get('ho')
    ten = request.json.get('ten')
    ngaySinh = request.json.get('ngaySinh')
    diaChi = request.json.get('diaChi')
    gioiTinh = request.json.get('gioiTinh')
    sdt = request.json.get('sdt')
    daNghiViec = request.json.get('daNghiViec')

    nhanVien = sessionDB.query(NHANVIEN).filter(NHANVIEN.ID == idnv).first()
    nhanVien.HO = ho
    nhanVien.TEN = ten
    nhanVien.NGAYSINH = ngaySinh
    nhanVien.DIACHI = diaChi
    nhanVien.GIOITINH = gioiTinh
    nhanVien.SDT = sdt
    nhanVien.DANGHIVIEC = daNghiViec

    try:
        sessionDB.commit()
    except Exception as e:
        sessionDB.rollback()
    finally:
        sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()


@employee_blueprint.route('/get' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def getEmployee():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)
    nhanViens = sessionDB.query(NHANVIEN).all()

    nhanVien_dicts = []
    for nhanVien in nhanViens:
        nhanVien_dict = {
            "ID": nhanVien.ID,
            "HO": nhanVien.HO,
            "TEN": nhanVien.TEN,
            "NGAYSINH": nhanVien.NGAYSINH,
            "DIACHI": nhanVien.DIACHI,
            "GIOITINH": nhanVien.GIOITINH,
            "SDT": nhanVien.SDT,
            "IDCONGTY": nhanVien.IDCONGTY,
            "DANGHIVIEC": nhanVien.DANGHIVIEC
        }
        nhanVien_dicts.append(nhanVien_dict)


    response = SuccessResponse(data=nhanVien_dicts)
    return response.toResponse()



