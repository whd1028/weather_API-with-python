from SqlConn import SqlConn

class WeatherSql:

    cursor = SqlConn.makeCursor()

    @staticmethod
    def insertData(tm,sumRn,ddMefs,ddMes,sumFogDur):
        # query = f"INSERT INTO weather VALUES ('{spot_num}','{YMD}','{HH}','{IO}','{lane}',{vol})"
        # WeatherSql.cursor.execute(query)
        # try:
        WeatherSql.cursor.execute("INSERT INTO weather VALUES (:1,:2,:3,:4,:5)",(tm,sumRn,ddMefs,ddMes,sumFogDur))  # Null값 입력을 위한 변경 (How_insert_Null.py참고)
        print("insert data")
        # except:
            # WeatherSql.cursor.execute("INSERT INTO weather VALUES (:1,:2,:3,:4,:5)",(tm,None,None,None,None)) 
        SqlConn.commit()
        # print("insertData")