import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder


######### mysql에서 데이터 불러오기
engine = create_engine(f'mysql+pymysql://root:kch41542672@localhost/movie?charset=utf8')
connect = engine.connect()
raw_data_set = pd.read_sql_table('review', connect)
#print(raw_data)


######### 만약 '괴물'이라는 영화 평이 1개라면 평가가 되나?


######### 디비 아이디는 버리기
data = raw_data_set
data = data.drop(['id'], axis = 1)
#print(data)


######## 중복값 없이 행개수
# all_user = data.user.unique().shape[0]
# all_movie = data.title.unique().shape[0]
#print(f'유저 수 {all_user}명, 영화 수 {all_movie}.')


######## 상위 이용 정리
# user_top_5 = data.user.value_counts()[:5]
# movie_top_5 = data.title.value_counts()[:5]
#print(user_top_5)
#print(movie_top_5)


######## show
# plt.style.use('ggplot')
# plt.figure(figsize=(10,10))
# user_top_5.plot(kind='bar', title='user', legend = True, fontsize = 10)
# plt.xticks(rotation = 0)
# plt.ylabel('Num of review', fontsize =10)
# plt.show()


# Colaborative Filtering
# 라벨링
def labeling(column_name):
    le = LabelEncoder()
    data_copy = data.copy()
    labeling_data = le.fit_transform(data_copy[column_name])
    data_label = pd.DataFrame(labeling_data, columns = [column_name+'_label'], index=data_copy.index)
    # print(labeling_data)
    return data_label

label_data_user = labeling('user')
label_data_title = labeling('title')
#print(label_data_user)

temp =data.copy()
temp = temp.drop(temp.columns[0], axis=1)
label_data_set = pd.concat([label_data_user, label_data_title, temp], axis=1)
# print(label_data_set)

movie_list = list(data.title.unique())
movie_list = sorted(movie_list, key= str)
# print(movie_list)
data_matrix = pd.DataFrame(columns=['user'] + movie_list)
# print(data_matrix)

user_num = len(label_data_set['user_label'].unique())
movie_num = len(label_data_set['title_label'].unique())
user_score_list = []
for num in range(user_num):
    user_score_list = [0 for i in range(movie_num)]
    temp1 = label_data_set[label_data_set['user_label'] == num]
    for j in temp1.index:
        user_score_list[temp1.loc[j]['title_label']] = temp1.loc[j]['score']
    data_matrix.loc[num] = [num] + user_score_list

# print(data_matrix)

