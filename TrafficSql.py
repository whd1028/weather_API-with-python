from SqlConn import SqlConn

class TrafficSql:

    cursor = SqlConn.makeCursor()

    @staticmethod
    def insertData(spot_num,YMD,HH,IO,lane,vol):
        # query = f"INSERT INTO cartraffic VALUES ('{spot_num}','{YMD}','{HH}','{IO}','{lane}',{vol})"
        # TrafficSql.cursor.execute(query)
        try:
            TrafficSql.cursor.execute("INSERT INTO cartraffic VALUES (:1,:2,:3,:4,:5,:6)",(spot_num,YMD,HH,IO,int(lane),int(vol)))  # Null값 입력을 위한 변경 (How_insert_Null.py참고)
        except:
            TrafficSql.cursor.execute("INSERT INTO cartraffic VALUES (:1,:2,:3,:4,:5,:6)",(spot_num,YMD,HH,IO,None,None)) 
        SqlConn.commit()
        # print("insertData")

    @staticmethod
    def selectData(spot_num,YMD,HH):  # (미완성)지점번호,날짜,시간을 이용한 검색
        query = f"SELECT * FROM cartraffic WHERE spot_num = {spot_num} and ymd = {YMD} and hh = {HH}"
        TrafficSql.cursor.execute(query)
        pass 

    @staticmethod
    def selectLatestDate():  # (미완성)
        pass