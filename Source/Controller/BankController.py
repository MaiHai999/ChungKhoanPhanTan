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

bank_blueprint = Blueprint('bank', __name__)

@bank_blueprint.route('/getBank' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def getBank():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    banks = sessionDB.query(NGANHANG).all()

    # Chuyển đổi danh sách các đối tượng ngân hàng thành JSON
    bank_list = [{"ID": bank.ID, "TENNGANHANG": bank.TENNGANHANG} for bank in banks]

    # Trả về danh sách ngân hàng trong response
    response = SuccessResponse(data=bank_list)
    return response.toResponse()

@bank_blueprint.route('/getBankAccount' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def getBankAccount():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)
    idndt = request.json.get('idNDT')
    tknhs = sessionDB.query(TAIKHOANNGANHANG).filter(TAIKHOANNGANHANG.IDNDT == idndt).all()
    account_list = [
        {
            "MATK": tknh.MATK,
            "TENTAIKHOAN": tknh.TENTAIKHOAN,
            "SODU": tknh.SODU,
            "IDNGANHANG": tknh.IDNGANHANG,
            "TENNGANHANG" : tknh.banks.TENNGANHANG
        }
        for tknh in tknhs
    ]

    response = SuccessResponse(data=account_list)
    return response.toResponse()

@bank_blueprint.route('/addBankAccount' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def addBankAccount():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    # Lấy dữ liệu từ yêu cầu JSON
    matk = request.json.get('matk')
    tentaikhoan = request.json.get('tentaikhoan')
    idndt = request.json.get('idndt')
    idnganhang = request.json.get('idnganhang')
    sodu = request.json.get('sodu')

    # Tạo đối tượng TAIKHOANNGANHANG mới
    new_account = TAIKHOANNGANHANG(
        MATK=matk,
        TENTAIKHOAN=tentaikhoan,
        IDNDT=idndt,
        IDNGANHANG=idnganhang,
        SODU=sodu
    )

    # Thêm đối tượng vào session và commit để lưu vào database
    sessionDB.add(new_account)
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()


@bank_blueprint.route('/deleteBankAccount' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def deleteBankAccount():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    # Lấy dữ liệu từ yêu cầu JSON
    matk = request.json.get('matk')

    tknh = sessionDB.query(TAIKHOANNGANHANG).filter(TAIKHOANNGANHANG.MATK == matk).first()
    sessionDB.delete(tknh)
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()


@bank_blueprint.route('/updateBankAccount' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def updateBankAccount():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    # Lấy dữ liệu từ yêu cầu JSON
    matk = request.json.get('matk')
    tentaikhoan = request.json.get('tentaikhoan')
    idndt = request.json.get('idndt')
    idnganhang = request.json.get('idnganhang')
    sodu = request.json.get('sodu')

    account = sessionDB.query(TAIKHOANNGANHANG).filter_by(MATK=matk).first()

    account.TENTAIKHOAN = tentaikhoan
    account.IDNDT = idndt
    account.IDNGANHANG = idnganhang
    account.SODU = sodu

    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()



