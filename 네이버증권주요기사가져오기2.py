# 셀레니움 브라우저의 동작을 자동화하는 패키지
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://finance.naver.com/'

# 브라우저 종료 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option('detach',True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# Selenium을 사용하여 웹 페이지에서 데이터를 수집할 때, 요청 사이에 텀(지연 시간)을 두는 것은 좋은 습관입니다. 이는 여러 가지 이유로 유용합니다:
# 이유
#  서버에 대한 부담 감소:
#   요청을 너무 빠르게 보내면 서버에 과부하를 일으킬 수 있습니다. 이는 서버가 IP를 차단하거나 요청을 제한할 수 있는 원인이 될 수 있습니다.
#  동적 콘텐츠 로딩:
#    웹 페이지의 콘텐츠가 JavaScript로 동적으로 로드되는 경우, 페이지가 완전히 로드될 때까지 기다리지 않으면 필요한 데이터를 가져오지 못할 수 있습니다.
#   디버깅:
#     코드의 실행 속도가 너무 빠르면, 디버깅이 어려울 수 있습니다. 텀을 두면 각 단계의 결과를 쉽게 확인할 수 있습니다.

# 페이지가 모두 로드될때 까지 최대 2초대기
driver.implicitly_wait(2)


news_list = driver.find_elements(By.CSS_SELECTOR,"#content > div.article > div.section > div.news_area._replaceNewsLink > div > ul > li")
print(news_list)

# 주요 기사 링크, 제목 가져오기
news_links = []
news_titles = []
for new in news_list :
  news_links.append(new.find_element(By.CSS_SELECTOR,"a").get_attribute('href'))
  news_titles.append(new.text)

# 주요 기사 내용 가져오기
news_contents = []
for news_link in news_links :
  news_content_html = requests.get(news_link)
  soup = BeautifulSoup(news_content_html.content,'lxml')
  news_content = soup.select_one('#dic_area')
  news_contents.append(news_content.text)

#
data = {
  'link' : news_links ,
  'title' : news_titles,
  'content' : news_contents
}

df = pd.DataFrame(data)
df.to_excel('주요뉴스기사.xlsx')

driver.quit()




