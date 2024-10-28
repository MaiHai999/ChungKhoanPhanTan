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

price_blueprint = Blueprint('price', __name__)


@price_blueprint.route('/getPrice' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def getPrice():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    macp = request.json.get('macp')
    listPrices = sessionDB.query(LICHSUGIA).filter(LICHSUGIA.IDCOPHIEU == macp).all()

    price_history = [
        {
            "NGAY": price.NGAY.strftime("%Y-%m-%d %H:%M:%S") if price.NGAY else None,
            "GIASAN": price.GIASAN,
            "GIATRAN": price.GIATRAN,
            "GIATHAMCHIEU": price.GIATHAMCHIEU,
            "ID": price.ID,
            "IDCOPHIEU": price.IDCOPHIEU,
        }
        for price in listPrices
    ]

    response = SuccessResponse(data=price_history)
    return response.toResponse()

@price_blueprint.route('/addPrice' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def addPrice():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    ngay = request.json.get('ngay')
    giasan = request.json.get('giasan')
    giatran = request.json.get('giatran')
    giathamchieu = request.json.get('giathamchieu')
    idcophieu = request.json.get('idcophieu')

    new_price = LICHSUGIA(
        NGAY=ngay,
        GIASAN=giasan,
        GIATRAN=giatran,
        GIATHAMCHIEU=giathamchieu,
        IDCOPHIEU=idcophieu
    )

    CommonUtiles.addCustom(new_price, sessionDB=sessionDB)

    try:
        sessionDB.commit()
    except Exception as e:
        print(e)
        sessionDB.rollback()
        response = InternalServerErrorResponse()
        return response.toResponse()
    finally:
        sessionDB.close()


    response = SuccessResponse()
    return response.toResponse()

@price_blueprint.route('/deletePrice' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def deletePrice():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    magia = request.json.get('magia')
    gia = sessionDB.query(LICHSUGIA).filter(LICHSUGIA.ID == magia).first()
    sessionDB.delete(gia)
    sessionDB.commit()
    sessionDB.close()

    response = SuccessResponse()
    return response.toResponse()

@price_blueprint.route('/updatePrice' , methods=['POST','GET'])
@handle_exceptions
@jwt_required()
def updatePrice():
    identity = get_jwt_identity()
    sessionDB = CommonUtiles.getSessionDB(identity)

    price_id = request.json.get('id')
    ngay = request.json.get('ngay')
    giasan = request.json.get('giasan')
    giatran = request.json.get('giatran')
    giathamchieu = request.json.get('giathamchieu')
    idcophieu = request.json.get('idcophieu')

    existing_price = sessionDB.query(LICHSUGIA).filter_by(ID=price_id).first()

    # Update the fields with the new values if provided
    if ngay is not None:
        existing_price.NGAY = ngay
    if giasan is not None:
        existing_price.GIASAN = giasan
    if giatran is not None:
        existing_price.GIATRAN = giatran
    if giathamchieu is not None:
        existing_price.GIATHAMCHIEU = giathamchieu
    if idcophieu is not None:
        existing_price.IDCOPHIEU = idcophieu

    # Commit the updated record to the database
    sessionDB.commit()



    response = SuccessResponse()
    return response.toResponse()






