import requests
import pandas as pd
import json
import sqlite3

# 영화진흥원 API Key
key1 = "07b226227bbd6d25557295cc1a4dc51f"
key2 = "574e463cead5b3a7567127ca677586fe"

# 불러올 데이터 날짜 지정 
date = pd.date_range(start='20200101', end='20210930')
datelist = date.strftime('%Y%m%d').to_list()

# 영화진흥원 API 
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"

# 위에서 설정한 기간동안의 1일 Boxoffice 데이터 받기 
def get_box() : 
    movielist = []
    for i in datelist : 
        param = {
            'key' : f'{key2}',
            'targetDt' : i,
            }
        rq = requests.get(url, params=param)
        raw = json.loads(rq.text)
        for movie in raw['boxOfficeResult']['dailyBoxOfficeList']:
            movielist.append(
                {
                    'rank': int(movie['rank']),
                    'rankInten': int(movie['rankInten']),
                    'rankOldAndNew': movie['rankOldAndNew'],
                    'movieCd': movie['movieCd'],
                    'movieNm': movie['movieNm'],
                    'openDt': movie['openDt'],
                    'salesAmt': int(movie['salesAmt']),
                    'salesShare': float(movie['salesShare']),
                    'salesInten': int(movie['salesInten']),
                    'salesChange': float(movie['salesChange']),
                    'salesAcc': int(movie['salesAcc']),
                    'audiCnt': int(movie['audiCnt']),
                    'audiInten': int(movie['audiInten']),
                    'audiChange': float(movie['audiChange']),
                    'audiAcc': int(movie['audiAcc']),
                    'scrnCnt': int(movie['scrnCnt']),
                    'showCnt': int(movie['showCnt'])
                }
            )
    return movielist

box = get_box()

# 데이터 저장을 위해 db 연결 
conn = sqlite3.connect('Project.db')
cur = conn.cursor()

# table 생성 
cur.execute("""CREATE TABLE boxoffice
(Id INTEGER PRIMARY KEY autoincrement,
Rank INTEGER,
RankInten INTEGER, 
RankOldAndNew TEXT,
MovieCd TEXT,
MovieNm TEXT,
OpenDt DATE,
SalesAmt INTEGER,
SalesShare NUMERIC,
SalesInten INTEGER,
SalesChange NUMERIC,
SalesAcc INTEGER,
AudiCnt INTEGER,
AudiInten INTEGER,
AudiChange NUMERIC,
AudiAcc INTEGER,
ScrnCnt INTEGER,
ShowCnt INTEGER);
""")

# 데이터 insert 
for value in box : 
    cur.execute("""INSERT INTO boxoffice 
    (Rank,
    RankInten,
    RankOldAndNew,
    MovieCd,
    MovieNm,
    OpenDt,
    SalesAmt,
    SalesShare,
    SalesInten,
    SalesChange,
    SalesAcc,
    AudiCnt,
    AudiInten,
    AudiChange,
    AudiAcc,
    ScrnCnt,
    ShowCnt)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
    list(value.values()))

    conn.commit()



