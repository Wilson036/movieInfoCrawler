import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import datetime as dt

url = 'https://movies.yahoo.com.tw/'
resp = requests.get(url)
resp.encoding = 'utf8'


soup = BeautifulSoup(resp.text, 'lxml')
movie_html = soup.find('select', attrs={'name': 'movie_id'})

movie_item = movie_html.find_all(
    'option', attrs={'data-name': re.compile('.*')})
# print(movie_item)

title_list = []
id_list = []

for info in movie_item:
    id_list.append(info["value"])
    title_list.append(info["data-name"])


df_movie_id = pd.DataFrame()
df_movie_id['title'] = title_list
df_movie_id['ID'] = id_list


# 找出上印中電影的id並產出excel
#df_movie_id.to_csv('./movie_id.csv', encoding="utf-8-sig")


def setHeader(target_id):
    return {
        'authority': 'movies.yahoo.com.tw',
        'method': 'GET',
        'path': '/api/v1/areas_by_movie_theater?movie_id=' + str(target_id),
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'avi=eyJpdiI6IlI0UUtyc1RJWUtsalwvRHFvTGcrbGlBPT0iLCJ2YWx1ZSI6Ik9DZVY0QnZWbXRORTRyVUxqODh2WVZ1RmNvelgrbE9kQmt4bW1KTmY3bDFOd3A1R0N3XC9BUStRZUxtUVNBZVhwIiwibWFjIjoiZjI0YjJjNDU0ZTVkNDFhNmZmYjNkNGNmZjEyN2IyM2RlMTA0ZTdlZTdiZjdlOTA4MTE5OTQ0OGI1MDY1YTFmZiJ9; BX=djffiohg5lpdc&b=3&s=0m; GUC=AQEBAQFgXDdgZEIkFgUa; A1=d=AQABBKzlWmACEP2syNlZ2__vFNITp8TyvdkFEgEBAQE3XGBkYAAAAAAA_SMAAAcIrOVaYMTyvdk&S=AQAAAuiqjiA7D5UWGw15F-nMy7s; A3=d=AQABBKzlWmACEP2syNlZ2__vFNITp8TyvdkFEgEBAQE3XGBkYAAAAAAA_SMAAAcIrOVaYMTyvdk&S=AQAAAuiqjiA7D5UWGw15F-nMy7s; A1S=d=AQABBKzlWmACEP2syNlZ2__vFNITp8TyvdkFEgEBAQE3XGBkYAAAAAAA_SMAAAcIrOVaYMTyvdk&S=AQAAAuiqjiA7D5UWGw15F-nMy7s&j=WORLD; rxx=sswrmbgrq9.29utaxj4&v=1; _ga=GA1.4.1292391094.1616569774; _gid=GA1.4.139633059.1616569774; __gads=ID=636d06331f8992ae-224f1fa4a7c60016:T=1616569779:RT=1616569779:S=ALNI_MbI1GJiFa-n9wkAZkCXCLlv66YxPQ; cmp=t=1616573554&j=0; b_m2=eyJpdiI6IlFXRXRBQUJPV2orc3EwTkV2T2pianc9PSIsInZhbHVlIjoiRzF5clNJWVNYNGpWc0dpOGI0QVU1dGFsdnI1cDB1TDJpY1I5c21DeFBuamJDR0JDOTgrXC9tZzBkTURVZlpqbUpTQ0JRVW9za0g2WDFyelU1clZSd2FzckhhZUNBcXhsVXBNXC9YZ21TNVFFNm03R0ZUMWY0UXJGNDg1RDF0WkpiYiIsIm1hYyI6IjhkMzNjZDI4YWVlMGRhY2E2M2U3NWMwMzFjN2M0ZGVmM2NjOGFiYmZiNWJkOGFjNWI1NzdkM2EyZDVjNWRhMDEifQ==; XSRF-TOKEN=eyJpdiI6ImlBRDlXRjNwK3VCWXFnUCt2dGtGWWc9PSIsInZhbHVlIjoiXC9ESlhOR2dnSEpWYWtZem1DZmZtOGE5MTl6UW1pNGlWRVFIWnhYWXpnamJId2FjNllOUkhrOTJ2YnRHQXViWVAiLCJtYWMiOiJmNTg2ZTNlZDM4NzFjNzRhMDA1MGRmZmJhYjJhMDQ0ZmEyZTc2MjgzMGI3MzY0OTU2MGQxMmJkNDcwZDFjNTBmIn0=; ms55=eyJpdiI6IndldzVydlZ2K1wvXC9ndXpXU2ZFN2VlZz09IiwidmFsdWUiOiIzcDgwYmRtcnJGRlY1MnFvdDFPVWcxRFk2K2lVNnY4YmZyZzJDU201dEx0dWVkNUtxVDRWcEp5NXp2QTRDQzRKbmdnSldreVdYWGRIa3psWVlqdldsTHRRU2tqc0dMb0ZvRk1qR2JMOExQMW5SQnBCZHpqU3JJcnR1empJMFBXMCIsIm1hYyI6IjM2NWYxZGUxZDZiN2UzNDMxM2Y1OWUxZGI0NDQ0MDgxNGY0ZmVmZDU2ZTlmNGQyY2YxZTcwZGFjNDZhYWI2MTIifQ==; _gat=1',
        'dnt': '1',
        'mv-authorization': '21835b082e15b91a69b3851eec7b31b82ce82afb',
        'referer': 'https://movies.yahoo.com.tw/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56',
    }


# 查詢電影放應地區
# movies_details = []
# url = 'https://movies.yahoo.com.tw/api/v1/areas_by_movie_theater'
# for i in range(len(id_list)):
#     target_id = id_list[i]
#     payload = {'movie_id': str(target_id)}
#     resp = requests.get(url, params=payload, headers=setHeader(target_id))
#     movie_dect = {}
#     movie_dect[target_id] = resp.json()
#     movies_details.append(movie_dect)
# print(movies_details)

# 向網站發送請求
# url = 'https://movies.yahoo.com.tw/movietime_result.html'
# payload = {'movie_id': str(target_id), 'area_id': str(area_id)}
# resp = requests.get(url, params=payload)
# resp.encoding = 'utf-8'
# print(resp.url)

# soup = BeautifulSoup(resp.text, 'lxml')
movie_date = soup.find_all('label', attrs={'for': re.compile('date_[\d]')})

# for date in movie_date:
#     print("{} {}".format(date.p.string, date.h3.string))

date1 = dt.today().strftime("%Y-%m-%d")

url = "https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie"
# time_dirc = {}
theater_list = {}
date_dict = {}
for i in range(3):
    delta_time = datetime.timedelta(days=i)
    new_day = dt.today() + delta_time
    date = new_day.strftime("%Y-%m-%d")
    payload = {'movie_id': str(11215),
               'date': date,
               'area_id': str(28),
               'theater_id': '',
               'datetime': '',
               'movie_type_id': ''}
    resp = requests.get(url, params=payload)
    json_data = resp.json()
    soup = BeautifulSoup(json_data['view'], 'lxml')
    html_elem = soup.find_all(
        "ul", attrs={'data-theater_name': re.compile(".*")})

    for the in html_elem:
        theater = the.find("li", attrs={"class": "adds"}).find("a")[
            'href'].partition("=")[2]
        info = the.find_all(class_="gabtn")
        time_list = []
        for i in info:
            time_dirc = {}
            time_dirc[i["data-movie_type"]] = i["data-movie_time"]
            time_list.append(time_dirc)
        theater_list[theater] = time_list
    date_dict[date] = theater_list
print(date_dict)


# 取得電影詳細資訊
# url = 'https://movies.yahoo.com.tw/movietime_result.html/id=11215'
# resp = requests.get(url)

# soup = BeautifulSoup(resp.text, 'lxml')
# print(soup.find('div', attrs={'class', 'inform_pic'}).find('img')['src'])
# print(soup.find('div', attrs={
#       'class', 'release_movie_time'}).text.strip().partition('上映日期：')[2])
# print(soup.find('div', attrs={'class', 'leveltext'}).find('span').text)
