from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time



# TIGER 2차전지 테마주
url = 'https://finance.naver.com/item/main.naver?code=305540'

# 브라우저 종료 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

driver.implicitly_wait(2)

news_list = driver.find_elements(By.CSS_SELECTOR, "div.sub_section:nth-child(1) ul > li")

# 주요 기사 링크, 제목 가져오기
news_links = []
news_titles = []
for new in news_list:
  news_links.append(new.find_element(By.CSS_SELECTOR, "a").get_attribute('href'))
  news_titles.append(new.text)

# 주요 기사 내용 가져오기
news_contents = []
for news_link in news_links:
  driver.get(news_link)  # Selenium으로 링크 열기
  time.sleep(2)  # 페이지 로드 대기
  soup = BeautifulSoup(driver.page_source, 'lxml')

  # 내용 가져오기
  news_content = soup.select_one('#dic_area')

  # 내용이 없을 때 None 체크
  if news_content:
    news_contents.append(news_content.text.strip())
  else:
    news_contents.append("내용을 가져올 수 없습니다.")  # 대체 텍스트 추가

# 데이터 프레임 생성
data = {
  'link': news_links,
  'title': news_titles,
  'content': news_contents
}

df = pd.DataFrame(data)
print(df)
df.to_excel('2차전지뉴스기사.xlsx')

driver.quit()