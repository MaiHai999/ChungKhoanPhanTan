from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash
from sqlalchemy.exc import NoResultFound

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort, redirect

from Source.Utiles.CustomResponse import *
from Source.Utiles.MyConnectPro import *
from Source.Utiles.MyConnect import *
from Source.Service.Models import *
from Source.Utiles.HandleExceptions import *
from Source.Utiles.CommonUtiles import *


import os
from Config import *

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login' , methods=['POST','GET'])
@handle_exceptions
def login():
    site = request.json.get('site')
    role = request.json.get('role')
    username = request.json.get('username')
    password = request.json.get('password')
    severName = None
    if site == SEVER_CONGTY_010:
        severName = os.environ.get("SEVER_NAME_CONGTY_010")
    elif site == SEVER_CONGTY_020:
        severName = os.environ.get("SEVER_NAME_CONGTY_020")
    elif site == SEVER_CONGTY_HNX:
        severName = os.environ.get("SEVER_NAME_CONGTY_HNX")
    else:
        raise ValueError("Lỗi")



    if role == ROLE_NDT and site != SEVER_CONGTY_HNX:
        userNameLoginSever = os.environ.get("USERNAME_NDT_010") if site == SEVER_CONGTY_010 else os.environ.get("USERNAME_NDT_020")
        passwordServer = os.environ.get("PASSWORD_NDT_010") if site == SEVER_CONGTY_010 else os.environ.get("PASSWORD_NDT_020")

        DBManager = MyConnectPro(user=userNameLoginSever, password=passwordServer, database='CHUNGKHOAN', server=severName, port=1433)
        DBManager.connect()
        sessionDB = DBManager.getSession()

        NhaDauTu = sessionDB.query(NDT).filter(NDT.CMND == username).first()
        if(NhaDauTu.MATKHAU == password):
            idenInfo = {
                "severName" : severName,
                "role" : ROLE_NDT,
                "userID" : NhaDauTu.MATK,
                "userName" : None,
                "passWord" : None,
            }
            accessToken = create_access_token(identity=idenInfo, fresh=True)
            data = {'access_token': accessToken}
            response = SuccessResponse(data=data)
            return response.toResponse()
        else:
            raise ValueError("Sai mật khẩu")
    elif role == ROLE_NV:
        DBManager = MyConnectPro(user=username, password=password, database='CHUNGKHOAN',server=severName, port=1433)
        DBManager.connect()
        DBManager.checkConnection()
        idenInfo = {
            "severName": severName,
            "role": ROLE_NV,
            "userID": None,
            "userName": username,
            "passWord": password,
        }
        accessToken = create_access_token(identity=idenInfo, fresh=True)
        data = {'access_token': accessToken}
        response = SuccessResponse(data=data)
        return response.toResponse()
    else:
        raise ValueError("Sai mật khẩu")

@auth_blueprint.route('/getLoginName' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def getLoginName():
    identity = get_jwt_identity()
    severName, role, userID, userName, passWord = CommonUtiles.getInfoLogin(identity)
    idnv = request.json.get('IDNV')
    param = {
        "username" : idnv
    }

    myDBmanager = MyConnect(user=userName, password=passWord, database="CHUNGKHOAN", server=severName)
    severnamePro = myDBmanager.callSP("SP_LAYLOGINNAME", param)

    if len(severnamePro) == 0:
        severname = None
    else:
        severname = severnamePro[0][0]

    data = {
        "userName" : severname
    }

    response = SuccessResponse(data=data)
    return response.toResponse()

@auth_blueprint.route('/createLogin' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def createLogin():
    identity = get_jwt_identity()
    severName, role, userID, userName, passWord = CommonUtiles.getInfoLogin(identity)
    lgname = request.json.get('lgname')
    passWord1 = request.json.get('passWord')
    username = request.json.get('username')

    spName = "SP_TAOLOGIN"

    params = {
        "lgname": lgname,
        "pass": passWord1,
        "username": username,
        "role": "CongTy" if severName != os.environ.get("SEVER_NAME_CONGTY_HNX") else "SoGD"
    }

    myDBmanager = MyConnect(user=userName, password=passWord, database="CHUNGKHOAN", server=severName)
    result = myDBmanager.callSP(spName, params)
    print(result)

    response = SuccessResponse()
    return response.toResponse()

@auth_blueprint.route('/deleteLogin' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def deleteLogin():
    identity = get_jwt_identity()
    severName, role, userID, userName, passWord = CommonUtiles.getInfoLogin(identity)
    lgname = request.json.get('lgname')
    usrname = request.json.get('username')

    spName = "SP_XOALOGIN"

    params = {
        "lgname": lgname,
        "usrname": usrname,
    }

    myDBmanager = MyConnect(user=userName, password=passWord, database="CHUNGKHOAN", server=severName)
    result = myDBmanager.callSP(spName, params)
    print(result)

    response = SuccessResponse()
    return response.toResponse()



