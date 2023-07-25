import sys
import os
import sqlite3
projectRoot = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(projectRoot)
from db.DBextractor import DBextractor
from input.precleaning import Precleaning


db_path = "data.db"
db_path2 = "data copy.db"
db_path3 = "dataword copy.db"


con = sqlite3.connect(db_path, isolation_level = None)
cur = con.cursor()

con2 = sqlite3.connect(db_path2, isolation_level = None)
cur2 = con2.cursor()

con3 = sqlite3.connect(db_path3, isolation_level = None)
cur3 = con3.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS data(title str, theme str, actor str, directer str, score str, time int, limit_age int, poster str, story str, storyWord str)")

cur2.execute("SELECT * FROM data")
datalist = cur2.fetchall()

cur3.execute("SELECT * FROM data")
storyWordlist = cur3.fetchall()

for i in range(0, len(datalist)):
    data = datalist[i]
    storyWord = storyWordlist[i]

    print(storyWord[0])
    title = data[0]
    theme = data[1]
    actor = data[2]
    director = data[3]
    score = int(data[4])
    time = int(data[5])
    limit_age = data[6]
    poster = data[7]
    story = data[8]

    cur.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, theme, actor, director, score, time, limit_age, poster, story, storyWord[0]))

    
con.close()
con2.close()
con3.close()


# # storyWord 컬럼 db 파일 생성
# db_path = "data.db"
# con = sqlite3.connect(db_path, isolation_level = None)
# cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS dataword(storyWord str)")
# storywordlist = Precleaning().getStoryList()
# for storyWord in storywordlist:
#     cur.execute("INSERT INTO dataword VALUES(?)", (storyWord,))
# con.close()




# db = DBextractor()
# # db.execute("ALTER TABLE data ADD COLUMN storyWord str")
# db.execute(f"UPDATE data SET storyWord = 'test' WHERE theme = 'ACTION'")
# db.conn.commit()

# del db