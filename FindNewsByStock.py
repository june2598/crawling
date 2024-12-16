from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time
import datetime

# 오늘 날짜 가져오기
today = datetime.datetime.today()
today = today.strftime('%Y-%m-%d')
new_file_name = f'final_etf_data_{today}.csv'

# 오늘 날짜의 ETF종목 데이터 가져오기
df = pd.read_csv(new_file_name)

# 브라우저 종료 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

# 종목명으로 해당하는 뉴스를 불러오는 함수
def find_news_by_stock(stock) :
  '''
  주어진 종목명에 대해 관련 뉴스 목록을 반환하는 함수.

  :param stock: 종목명 (str)
  :return:기사링크, 기사제목, 기사내용(df)
  '''
  if stock not in df['종목명'].values:
    raise ValueError

  url = df[df['종목명'] == stock]['link'].values[0]

  # 주요 기사 링크, 제목 가져오기
  news_links = []
  news_titles = []
  news_contents = []

  driver.get(url)
  driver.implicitly_wait(2)

  news_list = driver.find_elements(By.CSS_SELECTOR, "div.sub_section:nth-child(1) ul > li")

  for new in news_list:
    # 기사 링크 가져오기
    news_links.append(new.find_element(By.CSS_SELECTOR, "a").get_attribute('href'))
    # 기사 제목 가져오기
    news_titles.append(new.text)

    # 주요 기사 내용 가져오기
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

  news_df = pd.DataFrame(data)

  print(news_df)

# 함수 동작 테스트
find_news_by_stock('PLUS 200')

driver.quit()
