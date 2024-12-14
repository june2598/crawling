# http 요청을 보내고 응답을 처리할 때 사용 되는 패키지
import requests

# 구문 분석, 트리 탐색, 검색 및 수정에 사용 되는 패키지, 내부적으로 lxml, html5lib 패키지를 사용할 수 있다.
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://finance.naver.com/'
res = requests.get(url)
print(res.status_code)
print(res.text)
# print(res.content)

# ctrl+q : 문서보기
soup = BeautifulSoup(res.content, 'lxml')   #markup, 파서기
# firefox환경
# print(soup.select_one('.kospi_area > div:nth-child(1) > a:nth-child(2) > span:nth-child(1)'))

# bs4.select_one('css선택자')  : 하나 찾을때      (querySelector)
# bs4.select('css선택자') : 여러개 찾을때                      (querySelectorAll)

# 국내 KOSPI 지수 읽기
element = soup.select_one('#content > div.article > div.section2 > div.section_stock_market > div.section_stock > div.kospi_area.group_quot.quot_opn > div.heading_area > a > span > span.num')
print(element.text)

# 여러개 가져오면 리스트로 가져오는듯?
# 주요 기사 가져오기
item_list = soup.select('#content > div.article > div.section > div.news_area._replaceNewsLink > div > ul > li')
print(item_list)
print(len(item_list))


links = []
titles = []
for item in item_list :
  links.append(item.select_one('a[href]').attrs.get('href'))
  titles.append(item.select_one('a').text)

news_dict = dict(zip(links,titles))
print(news_dict)

news_bodies = []
for link in news_dict.keys() :
  news_bodies.append(requests.get(link).text)

print(len(news_bodies))

