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

@ndt_blueprint.route('/get' , methods=['POST','GET'])
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


    response = SuccessResponse()
    return response.toResponse()


