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

report_blueprint = Blueprint('report', __name__)

@report_blueprint.route('/getSohuu', methods=['POST', 'GET'])
@handle_exceptions
@jwt_required()
def getSohuu():
    identity = get_jwt_identity()
    severName, role, userID, userName, passWord = CommonUtiles.getInfoLogin(identity)

    idndt = request.json.get('idNDT') if role == ROLE_NV else userID
    userName = userName if role == ROLE_NV else os.environ.get("USERNAME_NDT_010")
    passWord = passWord if role == ROLE_NV else os.environ.get("PASSWORD_NDT_010")

    spName = "SP_SOHUUCOPHIEU"

    params = {
        "Mandt": idndt,
    }
    myDBmanager = MyConnect(user=userName, password=passWord, database="CHUNGKHOAN", server=severName)
    result = myDBmanager.callSP(spName, params)

    json_list = [
        {
            "MACP": item[0],
            "SOLUONG": item[1],
            "GIA": item[2],
            "GIATRI": item[3]
        }
        for item in result
    ]


    response = SuccessResponse(data=json_list)
    return response.toResponse()



@report_blueprint.route('/getSaoKe', methods=['POST', 'GET'])
@handle_exceptions
@jwt_required()
def getSaoKe():
    identity = get_jwt_identity()
    severName, role, userID, userName, passWord = CommonUtiles.getInfoLogin(identity)

    idndt = request.json.get('idNDT') if role == ROLE_NV else userID
    StartDate = request.json.get('StartDate')
    EndDate = request.json.get('EndDate')

    userName = userName if role == ROLE_NV else os.environ.get("USERNAME_NDT_010")
    passWord = passWord if role == ROLE_NV else os.environ.get("PASSWORD_NDT_010")

    spName = "SP_SOKELENHKHOP"

    params = {
        "IDNDT": idndt,
        'StartDate': StartDate,
        'EndDate' : EndDate
    }

    myDBmanager = MyConnect(user=userName, password=passWord, database="CHUNGKHOAN", server=severName)
    result = myDBmanager.callSP(spName, params)

    json_list = [
        {
            "NGAYKHOP": item[0].strftime("%Y-%m-%d %H:%M:%S"),
            "MACP": item[1],
            "LOAIGD": item[2],
            "LOAILENH": item[3],
            "SOLUONGKHOP" : item[4],
            "GIAKHOP" : item[5]
        }
        for item in result
    ]


    response = SuccessResponse(data=json_list)
    return response.toResponse()


@report_blueprint.route('/getCTKHOPLENH', methods=['POST', 'GET'])
@handle_exceptions
@jwt_required()
def getCTKHOPLENH():
    identity = get_jwt_identity()
    severName, role, userID, userName, passWord = CommonUtiles.getInfoLogin(identity)

    idndt = request.json.get('idNDT') if role == ROLE_NV else userID
    MACP = request.json.get('MACP')

    userName = userName if role == ROLE_NV else os.environ.get("USERNAME_NDT_010")
    passWord = passWord if role == ROLE_NV else os.environ.get("PASSWORD_NDT_010")

    spName = "SP_CTKHOPLENH"

    params = {
        "IDNDT": idndt,
        'MACP': MACP,
    }

    myDBmanager = MyConnect(user=userName, password=passWord, database="CHUNGKHOAN", server=severName)
    result = myDBmanager.callSP(spName, params)

    json_list = [
        {
            "NGAYKHOP": item[0].strftime("%Y-%m-%d %H:%M:%S"),
            "SOLUONGKHOP": item[1],
            "GIAKHOP": item[2],
        }
        for item in result
    ]

    response = SuccessResponse(data=json_list)
    return response.toResponse()