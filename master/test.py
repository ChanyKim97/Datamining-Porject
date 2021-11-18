import requests
from bs4 import BeautifulSoup
import re
import pymysql

# res = requests.get(f"http://movie.naver.com/movie/point/af/list.naver?st=nickname&sword=1&target=after")
# content = res.text
# soup = BeautifulSoup(content, 'html.parser')
#
# movie_links = soup.select('a[href]')
#
#
# movie_links_list = []
#
# for L in movie_links:
#     # list의 href부분에 search부분 포함된
#     if re.search(r'st=mcode&sword' and r'&target=after$', L['href']):
#         print(L)
#         target_url = 'http://movie.naver.com/movie/point/af/list.naver' + str(L['href'])
#         print(L['href'])
#         print(target_url)
#         movie_links_list.append(target_url)

# genre_list=[]
#
# res = requests.get("http://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=36944&target=after")
# content = res.text
# soup = BeautifulSoup(content, 'html.parser')
#
# genre = soup.find_all('table', 'info_area')
#
# print(genre)
#
# for G in genre:
#     genre_list.append(G.a.get_text())
#
# print(genre_list)

res = requests.get("https://movie.naver.com/movie/point/af/list.naver?st=nickname&sword=4&target=after&page=1")
content = res.text
soup = BeautifulSoup(content, 'html.parser')

#모든 a태그
page_links = soup.select('a[href]')
page_links_list=[]
for L in page_links:
    if re.search(r'&target=after&page', L['href']):
        target_url = 'http://movie.naver.com' + str(L['href'])
        page_links_list.append(target_url)

if len(page_links_list) > 1:
    pop_number = len(page_links_list) - 1
    page_links_list.pop(pop_number)

print(page_links_list)
