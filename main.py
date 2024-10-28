import Variable

from flask import Flask
from datetime import timedelta
import os
from flask_jwt_extended import JWTManager
from flask import jsonify
from flask_cors import CORS

from Source.Controller.AccountController import auth_blueprint
from Source.Controller.EmployeeController import employee_blueprint
from Source.Controller.NDTController import ndt_blueprint
from Source.Controller.BankController import bank_blueprint
from Source.Controller.StockController import stock_blueprint
from Source.Controller.PriceStockController import price_blueprint
from Source.Controller.OrderController import order_blueprint


app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CORS(app)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(employee_blueprint, url_prefix='/employee')
app.register_blueprint(ndt_blueprint, url_prefix='/ndt')
app.register_blueprint(bank_blueprint, url_prefix='/bank')
app.register_blueprint(stock_blueprint, url_prefix='/stock')
app.register_blueprint(price_blueprint, url_prefix='/price')
app.register_blueprint(order_blueprint, url_prefix='/order')
app.secret_key = os.environ.get("SECRET_KEY")

app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY_JWT")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True , port=9999)