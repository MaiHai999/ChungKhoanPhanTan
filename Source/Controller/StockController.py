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

stock_blueprint = Blueprint('stock', __name__)

@stock_blueprint.route('/addStock', methods=['POST'])
@handle_exceptions
@jwt_required()
def addStock():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    # Lấy dữ liệu từ yêu cầu JSON
    macp = request.json.get('macp')
    ten_cong_ty = request.json.get('ten_cong_ty')
    dia_chi = request.json.get('dia_chi')
    sdt = request.json.get('sdt')
    fax = request.json.get('fax')
    email = request.json.get('email')
    tong_so_luong_cp = request.json.get('tong_so_luong_cp')
    id_san = request.json.get('id_san')

    # Tạo đối tượng COPHIEU mới
    new_stock = COPHIEU(
        MACP=macp,
        TENCONGTY=ten_cong_ty,
        DIACHI=dia_chi,
        SDT=sdt,
        FAX=fax,
        EMAIL=email,
        TONGSOLUONGCP=tong_so_luong_cp,
        IDSAN=id_san
    )

    # Thêm đối tượng vào session và commit để lưu vào database
    sessionDB.add(new_stock)
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse(message="Stock added successfully.")
    return response.toResponse()


@stock_blueprint.route('/getStocks', methods=['POST', 'GET'])
@handle_exceptions
@jwt_required()
def getStocks():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    # Truy vấn tất cả cổ phiếu từ cơ sở dữ liệu
    stocks = sessionDB.query(COPHIEU).all()

    stock_list = [
        {
            "MACP": cp.MACP,
            "TENCONGTY": cp.TENCONGTY,
            "DIACHI": cp.DIACHI,
            "SDT": cp.SDT,
            "FAX": cp.FAX,
            "EMAIL": cp.EMAIL,
            "TONGSOLUONGCP": cp.TONGSOLUONGCP,
            "IDSAN": cp.IDSAN
        }
        for cp in stocks
    ]

    response = SuccessResponse(data=stock_list)
    return response.toResponse()


@stock_blueprint.route('/deleteStock', methods=['POST', 'GET'])
@handle_exceptions
@jwt_required()
def deleteStock():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    # Lấy dữ liệu từ yêu cầu JSON
    macp = request.json.get('macp')

    # Truy vấn cổ phiếu theo MACP
    stock = sessionDB.query(COPHIEU).filter(COPHIEU.MACP == macp).first()

    # Xóa cổ phiếu
    sessionDB.delete(stock)
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()


@stock_blueprint.route('/updateStock', methods=['POST', 'GET'])
@handle_exceptions
@jwt_required()
def updateStock():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    # Lấy dữ liệu từ yêu cầu JSON
    macp = request.json.get('macp')
    tencongty = request.json.get('tencongty')
    diachi = request.json.get('diachi')
    sdt = request.json.get('sdt')
    fax = request.json.get('fax')
    email = request.json.get('email')
    tongsoluongcp = request.json.get('tongsoluongcp')
    idsan = request.json.get('idsan')

    # Truy vấn cổ phiếu theo MACP
    stock = sessionDB.query(COPHIEU).filter_by(MACP=macp).first()

    # Cập nhật thông tin cổ phiếu
    stock.TENCONGTY = tencongty
    stock.DIACHI = diachi
    stock.SDT = sdt
    stock.FAX = fax
    stock.EMAIL = email
    stock.TONGSOLUONGCP = tongsoluongcp
    stock.IDSAN = idsan

    # Commit thay đổi vào cơ sở dữ liệu
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()

