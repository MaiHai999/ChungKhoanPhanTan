import pyodbc
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from Source.Service.Models import *

class MyConnectPro:
    def __init__(self, user, password, database, server, port):
        self.server = server  # Sử dụng server để chứa cả tên máy chủ và instance
        self.username = user
        self.password = password
        self.database = database
        self.port = port

    def connect(self):
        # Định dạng connection URL cho SQL Server
        connection_url = f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server"
        self.engine = create_engine(connection_url, echo=False, pool_recycle=3600)
        self.Session = sessionmaker(bind=self.engine)

    def checkConnection(self):
        with self.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    def getSession(self):
        session = self.Session()
        return session

    def executeQuery(self, query):
        if not self.engine or not self.Session:
            self.connect()
        session = self.Session()
        try:
            result = session.execute(text(query))
            return result.fetchall()
        finally:
            session.close()





# Sử dụng lớp MyConnectPro để kết nối và truy vấn
if __name__ == "__main__":
    # Thay thế các thông tin kết nối bằng thông tin của bạn
    my_db = MyConnectPro(user='sa', password='12', database='CHUNGKHOAN', server='DESKTOP-TQM3RV0\\SERVER0', port=1433)
    my_db.connect()
    sessionDB = my_db.getSession()

    listCY = sessionDB.query(NHANVIEN).all()
    for congty in listCY:
        print(congty.TEN)



