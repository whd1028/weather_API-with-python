# SqlConn.py
import cx_Oracle
import os

class SqlConn:
    LOCATION = r"C:\instantclient_19_12"
    os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]  #환경변수 등록
    username = "pjw"
    passwd ="pjw"
    connection = cx_Oracle.connect(username, passwd, 'localhost:1521/xe')

    @staticmethod
    def makeCursor():
        cursor = SqlConn.connection.cursor()
        return cursor
        
    @staticmethod
    def commit():
        SqlConn.connection.commit()
        
    @staticmethod
    def close():
        SqlConn.connection.close()



# 정상작동하는지 테스트용
if __name__ == "__main__":
    print("test")