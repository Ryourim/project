import sys
import os
projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(projectRoot)
import sqlite3

class DBextractor:
    # 생성자
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        if self.conn is None:
            print("[오류] DB 연결 실패")
            exit()
        self.cur = self.conn.cursor()

    # 쿼리 실행
    def execute(self, query):
        return self.cur.execute(query)

    # 커서 
    def getCursor(self):
        return self.cur

    # 다 쓰면 'del 객체이름' 적기~
    def __del__(self):
        self.conn.close()



########## 사용법 ##########
# import sys
# import os
# projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
# sys.path.append(projectRoot)
# from db.DBextractor import DBextractor

# 위는 각자 컴에 저장되어 있는 폴더 위치가 다를테니 디폴트 경로를 설정하는 코드
# 이 import문 작성 후 객체 생성해서 사용/다쓰고 del (precleaning.py 참고)