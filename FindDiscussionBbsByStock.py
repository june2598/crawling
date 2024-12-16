from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
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


def find_discussion_bbs_by_stock(stock):
  '''
  주어진 종목명에 대한 종목 토론실 링크를 반환하는 함수.

  :param stock: 종목명 (str)
  :return: 해당 종목의 토론실 링크 (str)
  '''
  if stock not in df['종목명'].values:
    raise ValueError(f"{stock}은 존재하지 않는 종목명입니다.")

  # 해당 종목 URL 가져오기
  url = df[df['종목명'] == stock]['link'].values[0]

  # 해당 종목 페이지로 이동
  driver.get(url)

  try:
    # 토론실 링크 주소 가져오기
    discussion_bbs_link = driver.find_element(By.CSS_SELECTOR, 'div.right:nth-child(2) > a:nth-child(4)').get_attribute('href')
    print(discussion_bbs_link)
  except Exception as e:
    print(f"토론실 링크를 찾는 중 오류가 발생: {e}")

# 함수 예시 사용
find_discussion_bbs_by_stock('PLUS 200')

# 웹 드라이버 종료
driver.quit()






