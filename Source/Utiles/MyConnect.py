
import pyodbc

class MyConnect:
    def __init__(self, user, password, database, server, port=None):
        self.server = server  # Sử dụng server để chứa cả tên máy chủ và instance
        self.username = user
        self.password = password
        self.database = database
        self.port = port

    def getConnection(self):
        connection = pyodbc.connect(
             f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
        )
        return connection

    def callSP(self, spName, params):
        connection = self.getConnection()
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            placeholders = ', '.join(['?' for _ in params])
            sql = f"EXEC {spName} {placeholders}"
            values = list(params.values())

            # Thực thi Stored Procedure
            cursor.execute(sql, *values)

            if cursor.description:
                result = cursor.fetchall()
            else:
                result = None

            return result
        except Exception as e:
            raise
        finally:
            cursor.close()
            connection.close()