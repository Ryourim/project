import time as t
import sqlite3
import requests
import json

db_path = "data.db"

"""
data.db
    data
        title, theme, actor, director, score, time, limit_age, poster, story
"""
idnum = 1

def write(id: int, title: str, theme: str, actor: str, director: str, score: str, time: int, limit_age: int, poster: str, story: str,):
    global idnum

    con = sqlite3.connect(db_path, isolation_level = None)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id int, title str, theme str, actor str, directer str, score str, time int, limit_age int, poster str, story str)")

# 같은 줄거리가 있는지 찾고 거르기
    cur.execute("SELECT * FROM data WHERE story=:story", {"story": story})
    duplicate_data = cur.fetchone()
    if duplicate_data:
        print("Duplicate data found. Skipping...")
        con.close()
        return


    cur.execute("SELECT * FROM data WHERE title=:title", {"title": title})
    data = cur.fetchone()
    if data is None:
        idnum += 1
        cur.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, title, theme, actor, director, score, time, limit_age, poster, story))
    else:
        t = ','.join(set(data[2].split(",") + [theme]))
        cur.execute("UPDATE data SET theme=:theme WHERE title=:title", {"theme": t, "title": title})
    
    con.close()
    

 
    
category_list = ["ACTION", "COMEDY", "DRAMA", "MELO", "HORROR", "SF_FANTASY", "ANIMATION", "DOCUMENTARY", "INDIE", "PERFORMANCE"]
for category in category_list:
    default_link = f"https://apis.naver.com/seriesOnWeb/serieson-web/v3/movie/products?categoryType={category}"

    count = 0
    while True:
        # 링크 만들기
        link = default_link + f"&orderType=RECENT_REGISTRATION&offset={count}&limit=100&tvod=true"
        # 웹에서 정보 가져오기
        response = requests.get(link)
        # json을 파싱해서 dict로 만들기
        data = json.loads(response.text)
        # 더 이상 정보가 없으면 break
        if data["result"].get("productList") == []:
            break

        for movie in data["result"]["productList"]:
            title = movie["product"]['meta']['name']
            theme = category
            actor = ','.join(movie["product"]['meta']['actors'])
            director = ','.join(movie["product"]['meta']['directors'])
            score = movie["product"]['meta']["starScore"]
            time = int(movie["product"]['meta']['screeningTimeMinute'])
            limit_age = int(movie['product']['meta']['contentRating']['accessibleAge'])
            poster = movie["product"]["meta"]["posterUrl"]
            story = movie["product"]['meta']['synopsis'].strip()

            write(idnum, title, theme, actor, director, score, time, limit_age, poster, story)
            print((idnum, title, theme, actor, director, score, time, limit_age, poster, story))

        
        count += 100

        t.sleep(0.7)