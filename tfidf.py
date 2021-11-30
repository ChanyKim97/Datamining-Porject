import pymysql
import math
import re

try:
    db = pymysql.connect(host='localhost', user='root', password='kch41542672', database='movie')
    cursor = db.cursor()
except Exception as p:
    print(p)

# ----------------------
# 전체 영화 보여주기
qry2 = "select title from temp_"
cursor.execute(qry2)
result = cursor.fetchall()
# print(result)
tmp_list = []

# tuple 형식의 데이터를 str로 변경 및 정규 표현식을 사용하여 문자열 치환
for i in range(len(result)):
    tmp_list.append(re.sub("\(|\)|\'","",str(result[i]))[:-1])

movie_list = ['head'] # 0번째 값엔 'head' 값을 둠 -> 1번째 값 부터 넣기 위해
movie_list.extend(list(set(tmp_list))) # 중복 데이터 제거, 집합은 idx 로 접근이 불가하기 때문에 idx로 접근이 가능한 리스트 형식으로 재변환

#for idx, title in enumerate(movie_list[1:]): # 첫째값이 '0 :' 이 아닌 '1 :' 로 하기 위해
#    print(" {} : \t {}".format(idx + 1, title))

# -----------------(1) 선호하는 영화(들) 선택--------------------
print("위 목록 중 선호하는 영화의 개수를 선택해 주세요 :")
num_of_prefers = int(input())
print("선호하는 영화의 번호를 입력해주세요 : ")
while 1:
    choices = list(map(int, input().split()))
    try:
        if len(choices) != num_of_prefers:
            raise ValueError
        break
    except ValueError:
        print("선호하는 영화의 개수가 일치하지 않습니다. 다시 입력해 주세요 :")
prefers = []
for num in choices: prefers.append(movie_list[num])
result = []
for i in range(num_of_prefers):
    qry3 = """select plot from temp_ where title='{}'""".format(prefers[i])
    cursor.execute(qry3)
    result.append(cursor.fetchall()[0]) # 중복 데이터를 제외

prefers_words_list = []

    # tuple 형식의 데이터를 str로 변경 및 정규 표현식을 사용하여 문자열 치환
for i in range(len(result)):
    prefers_words_list.append(re.compile('[가-힣]+').findall(str(result[i])))

# -----------------(2) 선호하는 영화 줄거리들의 TF 계산--------------------
prefers_words_dict = dict()
for words in prefers_words_list:
    for word in words:
        if word not in prefers_words_dict:
            prefers_words_dict[word] = 1
        else: prefers_words_dict[word] += 1

# -----------------(3) IDF 계산--------------------
qry = "select plot from temp_"
cursor.execute(qry)
result = cursor.fetchall()
words_list = []

db.close()

# DF : 문서의 수 / 특정 단어가 등장한 문서의 수
# tuple 형식의 데이터를 str로 변경 및 정규 표현식을 사용하여 문자열 치환
for i in range(len(result)):
    words_list.append(re.compile('[가-힣]+').findall(str(result[i])))

# 선호하는 영화 줄거리들에 포함된 단어들의 IDF 계산

num_of_docs = len(words_list)
words_dict = dict()

for word in prefers_words_dict:
    cnt = 0
    for words in words_list:
        if word in words: cnt += 1
    words_dict[word] = math.log(num_of_docs/(1 + cnt)) # IDF

# -----------------(4) 선호하는 영화 줄거리들의 TF-IDF를 계산--------------------
tf_idf_dict = dict()
for word in prefers_words_dict:
    tf_idf_dict[word] = prefers_words_dict[word] * words_dict[word] # TF * IDF
print(tf_idf_dict)

tf_idf_dict_sorted = sorted(tf_idf_dict.items(), key = lambda item: item[1])

for word in tf_idf_dict_sorted:
    print(f"{word[0]}: \t {word[1]}")