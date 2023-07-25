import sys
import os
projectRoot = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(projectRoot)
from db.DBextractor import DBextractor
from konlpy.tag import Okt
import re

class Precleaning:
    # 전처리한 줄거리 문자열 리스트 생성
    def getStoryList(self):
        db = DBextractor()
        db.execute("SELECT story FROM data")
        strList = []
        for row in db.getCursor():
            story = row[0]
            strList.append(self.preclean(story))
        del db
        return strList
    
    # 전처리 파트
    def preclean(self, story):
        okt = Okt()
        wordList = []
        # 특수문자, 줄바꿈 제거
        newStr = re.sub(r"[,./?!‘’“”\\<>\[\]@#$%^&*();:'\-+=_…]", "", story)
        newStr = re.sub("\n", " ", newStr)

        # 형태소분석기 활용해서 조사, 구두점, 외국어, 초성, 접미사, 부사가 아니면 wordList에 저장
        for word in okt.pos(newStr, stem=True):
            if word[1] not in ['Josa', 'Punctuation', 'Foreign', 'KoreanParticle', 'Suffix', 'Adverb']:
                wordList.append(word[0])

        # 불용어 처리 추가 부분
        with open('input/stopwords.txt', 'r', encoding='utf-8') as file:
            stopwords = file.read().splitlines()
        filteredList = [word for word in wordList if not word in stopwords]

        # 단어 리스트를 한 문장으로 만드는 부분
        listStr = " ".join(filteredList)
        return listStr