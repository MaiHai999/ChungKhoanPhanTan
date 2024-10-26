
from Source.Utiles.MyConnectPro import *
from Config import *
import os

class CommonUtiles:

    @staticmethod
    def getSessionDB(identity):
        severName = identity["severName"]
        role = identity["role"]
        userID = identity["userID"]
        userName = identity["userName"]
        passWord = identity["passWord"]

        if role == ROLE_NDT:
            userNameLoginSever = os.environ.get("USERNAME_NDT_010") if severName == os.environ.get("SEVER_NAME_CONGTY_010") else os.environ.get("USERNAME_NDT_020")
            passwordServer = os.environ.get("PASSWORD_NDT_010") if severName == os.environ.get("SEVER_NAME_CONGTY_020") else os.environ.get("PASSWORD_NDT_020")
            DBManager = MyConnectPro(user=userNameLoginSever, password=passwordServer, database='CHUNGKHOAN', server=severName, port=1433)
            DBManager.connect()
            DBManager.checkConnection()
            sessionDB = DBManager.getSession()
            return sessionDB
        else:
            DBManager = MyConnectPro(user=userName, password=passWord, database='CHUNGKHOAN', server=severName,port=1433)
            DBManager.connect()
            DBManager.checkConnection()
            sessionDB = DBManager.getSession()
            return sessionDB

    @staticmethod
    def addCustom(entity, sessionDB):
        # Lấy tên lớp (tên bảng)
        table_name = entity.__class__.__tablename__

        # Lấy các thuộc tính và giá trị, bỏ qua những thuộc tính có giá trị None
        columns = []
        values = {}

        for column in entity.__class__.__table__.columns:
            value = getattr(entity, column.name)
            if value is not None:  # Bỏ qua các thuộc tính có giá trị None
                columns.append(column.name)
                values[column.name] = value

        # Tạo câu lệnh SQL
        columns_str = ', '.join(f"[{col}]" for col in columns)
        placeholders_str = ', '.join(':' + col for col in columns)

        sql = f"INSERT INTO [{table_name}] ({columns_str}) VALUES ({placeholders_str})"
        sessionDB.execute(text(sql), values)
