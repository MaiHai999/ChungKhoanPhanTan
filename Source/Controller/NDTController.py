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
from Source.Utiles.MyConnect import *

ndt_blueprint = Blueprint('ndt', __name__)

def ndtToDict(ndt):
    return {
        "MATK": ndt.MATK,
        "HO": ndt.HO,
        "TEN": ndt.TEN,
        "NGAYSINH": ndt.NGAYSINH.strftime("%Y-%m-%d %H:%M:%S") if ndt.NGAYSINH else None,
        "NOISINH": ndt.NOISINH,
        "GIOITINH": ndt.GIOITINH,
        "DIACHI": ndt.DIACHI,
        "EMAIL": ndt.EMAIL,
        "CMND": ndt.CMND,
        "NGAYCAP": ndt.NGAYCAP.strftime("%Y-%m-%d %H:%M:%S") if ndt.NGAYCAP else None,
        "MATKHAU": ndt.MATKHAU,
        "IDCONGTY": ndt.IDCONGTY,
        "MATKHAUDATLENH": ndt.MATKHAUDATLENH
    }

@ndt_blueprint.route('/getNDT' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def getNDT():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)
    nhaDauTus = sessionDB.query(NDT).all()
    list_nha_dau_tu = [ndtToDict(ndt) for ndt in nhaDauTus]

    response = SuccessResponse(data=list_nha_dau_tu)
    return response.toResponse()


@ndt_blueprint.route('/add' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def addNDT():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)
    congty = sessionDB.query(CONGTYCK).first()

    ho = request.json.get('ho')
    ten = request.json.get('ten')
    ngaysinh = request.json.get('ngaysinh')
    noisinh = request.json.get('noisinh')
    gioitinh = request.json.get('gioitinh')
    diachi = request.json.get('diachi')
    email = request.json.get('email')
    cmnd = request.json.get('cmnd')
    ngaycap = request.json.get('ngaycap')
    matkhau = request.json.get('matkhau')
    idcongty = congty.ID
    matkhaudatlenh = request.json.get('matkhaudatlenh')

    nhadautu = NDT(
        HO=ho,
        TEN=ten,
        NGAYSINH=ngaysinh,
        NOISINH=noisinh,
        GIOITINH=gioitinh,
        DIACHI=diachi,
        EMAIL=email,
        CMND=cmnd,
        NGAYCAP=ngaycap,
        MATKHAU=matkhau,
        IDCONGTY=idcongty,
        MATKHAUDATLENH=matkhaudatlenh
    )

    CommonUtiles.addCustom(nhadautu, sessionDB)
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()


@ndt_blueprint.route('/delete' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def deleteNDT():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)
    idNDT = request.json.get('idNDT')
    nhadaut = sessionDB.query(NDT).filter(NDT.MATK == idNDT).first()
    sessionDB.delete(nhadaut)
    sessionDB.commit()

    response = SuccessResponse()
    return response.toResponse()


@ndt_blueprint.route('/update' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def dupdateNDT():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    idNDT = request.json.get('idNDT')
    ho = request.json.get('ho')
    ten = request.json.get('ten')
    ngaysinh = request.json.get('ngaysinh')
    noisinh = request.json.get('noisinh')
    gioitinh = request.json.get('gioitinh')
    diachi = request.json.get('diachi')
    email = request.json.get('email')
    cmnd = request.json.get('cmnd')
    ngaycap = request.json.get('ngaycap')
    matkhau = request.json.get('matkhau')
    matkhaudatlenh = request.json.get('matkhaudatlenh')

    nhadaut = sessionDB.query(NDT).filter(NDT.MATK == idNDT).first()
    nhadaut.Ho = ho
    nhadaut.TEN = ten
    nhadaut.NGAYSINH = ngaysinh
    nhadaut.NOISINH = noisinh
    nhadaut.GIOITINH = gioitinh
    nhadaut.DIACHI = diachi
    nhadaut.EMAIL = email
    nhadaut.CMND = cmnd
    nhadaut.NGAYCAP = ngaycap
    nhadaut.MATKHAU = matkhau
    nhadaut.MATKHAUDATLENH = matkhaudatlenh

    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()




