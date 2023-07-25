import sqlite3


class input:

    def search_term_count(column_name, search_term, db_path):
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # 열에 대해 검색어가 일치하는 행의 개수 가져오기
        cur.execute(f"SELECT COUNT(*) FROM data WHERE {column_name} LIKE '%{search_term}%'")
        count = cur.fetchone()[0]

        con.close()
        return count


    
    def search_term_moviedata(column_name, search_term, db_path):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        # 해당 컬럼의 영화 목록 가져오기
        cur.execute(f"SELECT * FROM data WHERE {column_name} LIKE '%{search_term}%'")
        movie_data = cur.fetchall()

        con.close
        return movie_data


    db_path = "data.db"
    
    con = sqlite3.connect(db_path, isolation_level = None)
    cur = con.cursor()

    search_term = input("검색어를 입력해주세요: ")

    title_count = search_term_count("title", search_term, db_path)
    actor_count = search_term_count("actor", search_term, db_path)


    if title_count >= actor_count and (title_count != 0 and actor_count != 0):
        # 검색어에 해당
        print("영화 제목 기반으로 검색")
        movie = search_term_moviedata("title", search_term, db_path)
        print(movie)

        # 이후 유사도 기반 영화 목록 추가하기
    
    elif title_count < actor_count:
        print("영화 배우 기반으로 검색")
        movie = search_term_moviedata("actor", search_term, db_path)
        print(movie)

        # 이후 유사도 기반 영화 목록 추가하기

    else:
        # 둘 다 결과가 없을 때
        # 전처리후 상위키워드로 word2vec으로 유사영화 추천
        print("pass")
        pass



    