import pymysql
from bs4 import BeautifulSoup
import requests
import re

# 줄거리 받아오기
def get_plots(url):
    res = requests.get(url)
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    try:
        return soup.select_one('p.con_tx').get_text()
    except AttributeError as e:
        print(e)
        return None

code_list = []

try:
    db = pymysql.connect(host='localhost', user='root', password='kch41542672', database='movie')
    cursor = db.cursor()
except Exception as p:
    print(p)

qry = "select movie_id from temp_"
cursor.execute(qry)
result = cursor.fetchall()
print(result)

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
for cd in code_list:
    url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={cd}"
    plots = get_plots(url)
    print(cd, plots, sep='\n')
    qry = """update temp_ set plot = ('{}') where movie_id = ('{}')""".format(plots, cd)
    try:
        db.commit()
        cursor.execute(qry)
    except Exception:
        pass

db.close()