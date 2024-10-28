from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from datetime import datetime
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort, redirect

from Source.Utiles.CustomResponse import *
from Source.Service.Models import *
from Source.Utiles.HandleExceptions import *
from Source.Utiles.CommonUtiles import *
from Source.Utiles.MyConnect import *

order_blueprint = Blueprint('order', __name__)

@order_blueprint.route('/addOrder' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def addOrder():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    matknh = request.json.get('matknh')
    macp = request.json.get('macp')
    loailenh = request.json.get('loailenh')
    loaigd = request.json.get('loaigd')
    soluong = request.json.get('soluong')
    ngaydatlenh = datetime.now()
    gia = request.json.get('gia')

    new_order = LENHDAT(
        MATKNH=matknh,
        MACP=macp,
        LOAILENH=loailenh,
        LOAIGD=loaigd,
        SOLUONG=soluong,
        TRANGTHAI=None,
        NGAYDATLENH=ngaydatlenh,
        GIA=gia
    )

    CommonUtiles.addCustom(entity=new_order,sessionDB=sessionDB)
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()