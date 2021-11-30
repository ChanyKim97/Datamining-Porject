import requests
from bs4 import BeautifulSoup
import re
import pymysql

#유저가 평가를 한 영화의 link를 받아오는 함수
def get_userreview_moive_link(url):

    #html 내용 받아오기
    res = requests.get(url)
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')

    #page a태그 href링크 있는 태그 불러오기
    page_all_movie_list = soup.select('a[href]')

    Review_movie_links_list = []
    for L in page_all_movie_list:
        #list의 href부분에 search부분 포함된
        if re.search(r'st=mcode&sword' and r'&target=after$', L['href']):
            target_url = 'http://movie.naver.com/movie/point/af/list.naver'+str(L['href'])
            Review_movie_links_list.append(target_url)

    return Review_movie_links_list


#위 함수로 부터 받은 영화 리스트의 장르를 가져오기
# def genre_list(url):
#     Review_movie_links_list = get_userreview_moive_link(url)
#
#     genre_list=[]
#
#     for url in Review_movie_links_list:
#         res = requests.get(url)
#         content = res.text
#         soup = BeautifulSoup(content, 'html.parser')
#
#         #table tag info_area class가진 부분
#         info = soup.find_all('table', 'info_area')
#
#         #첫번째 장르 종류
#         for G in info:
#             genre_list.append(G.a.get_text())
#
#     return genre_list
def genre_list_with_code(url):
    Review_movie_links_list = get_userreview_moive_link(url)
    genre_list = []
    movie_code_list = []
    for url in Review_movie_links_list:

        res = requests.get(url)
        content = res.text
        soup = BeautifulSoup(content, 'html.parser')

        # table tag info_area class가진 부분
        info = soup.find_all('table', 'info_area')
        code = soup.find_all('h5')

        # 첫번째 장르 종류
        for G in info:
            genre_list.append(G.a.get_text())

        for G in code:
            if G.a:
                movie_code_list.append(re.findall("[0-9]+", str(G.a))[0])


    return genre_list, movie_code_list


#유저의 평가 페이지 모두 가져오기
def get_userreview_page_all(url):
    res = requests.get(url)
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')

    #모든 a태그
    page_links = soup.select('a[href]')
    page_links_list=[]
    
    #인당 최대 100개
    for L in page_links:
        if re.search(r'&target=after&page', L['href']):
            target_url = 'http://movie.naver.com' + str(L['href'])
            page_links_list.append(target_url)
    
    #다음페이지 있으면 다음버튼때문에 한페이지 정보 더가져와서 삭제
    if len(page_links_list) > 1:
        pop_number = len(page_links_list) - 1
        page_links_list.pop(pop_number)

    return page_links_list


def do_crawling(url):
    url_list = get_userreview_page_all(url)
    db = pymysql.connect(host='localhost', user='root', password='kch41542672', database='movie')
    cursor = db.cursor()

    #평가 영화 10개 이상인 사람만 check
    if(len(url_list)) >=2:
        for url in url_list:
            genre_list_, movie_code_list_ = genre_list_with_code(url)

            res = requests.get(url)
            content = res.text
            soup = BeautifulSoup(content, 'html.parser')

            #평가한 사람 class author
            user_name = soup.find_all('a','author')
            movie_title = soup.find_all('a','movie color_b')
            user_score = soup.find_all('div', 'list_netizen_score')

            name_list = []
            for name in user_name:
                first_4_name = re.sub(r'[*]', '', name.get_text())
                name_list.append(first_4_name)

            title_list = []
            for title in movie_title:
                title_list.append(title.get_text())

            score_list = []
            for score in user_score:
                score_list.append(score.select('em')[0].contents[0])

            for num in range(len(title_list)):
                query = """insert into temp_ (user, title, movie_id, genre, score) values ('{}', '{}', '{}', '{}', '{}')""".format(
                    name_list[num], title_list[num], movie_code_list_[num], genre_list_[num], score_list[num])
                try:
                    db.commit()
                    cursor.execute(query)
                except Exception as e:
                    print(str(e))
                    db.rollback()

    db.close()


from concurrent.futures import ThreadPoolExecutor

#11/21 오후 06:55기준
#으로부터 댓글 1000개 가량 받아오기
#댓글 fix값 17810530 ~ 17809500
#tuple 총 13999개

page = 17810530
while page >17810500:
  page=str(page)
  url = f"http://movie.naver.com/movie/point/af/list.naver?st=nickname&sword={page}&target=after"

  with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(do_crawling, url)
    print(page)
    page = int(page)
    page -= 1