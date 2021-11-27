import pymysql
import math
import re

try:
    db = pymysql.connect(host='localhost', user='root', password='Gjs114268#', database='movie_db')
    cursor = db.cursor()
except Exception as p:
    print(p)

qry = "select plot from movie"
cursor.execute(qry)
result = cursor.fetchall()

db.close()

words_list = []

# tuple 형식의 데이터를 str로 변경 및 정규 표현식을 사용하여 문자열 치환
for i in range(len(result)):
    words_list.append(re.compile('[가-힣]+').findall(str(result[i])))

cnt = 0
words_dict = dict()

for words in words_list:
    for word in words:
        cnt += 1
        if word not in words_dict:
            words_dict[word] = 1
        else: words_dict[word] += 1

print(words_dict)
for word in words_dict:
    words_dict[word] = math.log(cnt/words_dict[word]) #IDF

print(words_dict)