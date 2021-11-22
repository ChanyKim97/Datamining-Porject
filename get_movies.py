# 1. DB 에서 가져온 영화 리스트를 set화
# 2. 영화마다 출연한 배우들 받아옴

import pymysql
from bs4 import BeautifulSoup
import requests
import re

def get_actors(url):
    actors = ''
    res = requests.get(url)
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    info = soup.select_one('dl.info_spec')
    try:
        actors_info = info.select('dd>p>a')
    except AttributeError as e:
        print(e)
        return ""

    for i in range(len(actors_info) - 1):
        nm = actors_info[i].get_text()
        actors += (nm + ',')

    actors = actors[:-1]

    return actors

code_list = []

try:
    db = pymysql.connect(host='localhost', user='root', password='Gjs114268#', database='movie_db')
    cursor = db.cursor()
except Exception as p:
    print(p)

qry = "select id from movie"
cursor.execute(qry)
result = cursor.fetchall()

for i in range(len(result)):
    code_list.append("".join(result[i]))

# qry = "select id from movie where actors is null"
# cursor.execute(qry)
# result = cursor.fetchall()
# for i in range(len(result)):
#     code_list.append("".join(result[i]))

# 리스트 to 집합으로 중복값 제거
code_list = set(code_list)

# # movie_db 에 있는 movie 테이블에 actors 필드의 values 넣기
# for cd in code_list:
#     url = f"https://movie.naver.com/movie/bi/mi/detail.naver?code={cd}"
#     actors = get_actors(url)
#     qry = """update movie set actors = ('{}') where id = ('{}')""".format(actors, cd)
#     try:
#         db.commit()
#         cursor.execute(qry)
#     except Exception:
#         pass

db.close()

