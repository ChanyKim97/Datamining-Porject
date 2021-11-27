import pymysql
import math
import re

try:
    db = pymysql.connect(host='localhost', user='root', password='Gjs114268#', database='movie_db')
    cursor = db.cursor()
except Exception as p:
    print(p)

qry = "select actors from movie"
cursor.execute(qry)
result = cursor.fetchall()

db.close()
actor_list = []

# tuple 형식의 데이터를 str로 변경 및 정규 표현식을 사용하여 문자열 치환
for i in range(len(result)):
    actor_list.append(re.sub("\(|\)|\'","",str(result[i])).split(',')[:-1])

cnt = 0
actor_dict = dict()

for actors in actor_list:
    for actor in actors:
        cnt += 1
        if actor not in actor_dict:
            actor_dict[actor] = 1
        else: actor_dict[actor] += 1

print(actor_dict)
for actor in actor_dict:
    actor_dict[actor] = math.log(cnt/actor_dict[actor]) #IDF

print(actor_dict)