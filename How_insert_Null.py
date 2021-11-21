import cx_Oracle
import os

LOCATION = r"C:\instantclient_19_12"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]  #환경변수 등록
username = "pjw"
passwd ="pjw"
connection = cx_Oracle.connect(username, passwd, 'localhost:1521/xe')
cursor = connection.cursor()

# 1. 
spot_num = '\'test1\''
YMD = '\'test1\''
HH = '\'test1\''
IO = 'null'
lane = 'null'
vol = 999
query = f"INSERT INTO cartraffic VALUES ({spot_num},{YMD},{HH},{IO},{lane},{vol})"
print(query)
cursor.execute(query)

# 2.
a = ('test2','test2','test2','test2',None,None)
print(query)
cursor.execute("INSERT INTO cartraffic VALUES (:1,:2,:3,:4,:5,:6)",a)

# 3. 출처 = {https://stackoverflow.com/questions/5507948/how-can-i-insert-null-data-into-mysql-database-with-python}
# value = None
# cursor.execute("INSERT INTO table (`column1`) VALUES (%s)", (value,))

connection.commit()
connection.close()
