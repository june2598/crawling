from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import datetime

'''
실시간 검색 상위 30종목의 간단한 정보를 가져오는 기능 구현
'''

chrome_option = Options()
chrome_option.add_experimental_option('detach',True)
driver = webdriver.Chrome(options=chrome_option)

# 네이버 페이 증권 검색 상위 종목 상위 30
url = 'https://finance.naver.com/sise/lastsearch2.naver'

driver.get(url)
driver.implicitly_wait(2)

trs = driver.find_elements(By.CSS_SELECTOR,'#contentarea > div.box_type_l > table > tbody > tr')

# html 페이지 분석 -> 유효한 행은 td수가 12개
popular_rows = [tr for tr in trs if len(tr.find_elements(By.TAG_NAME,'td')) == 12]

popular_data = []

for tr in popular_rows:
  cols = tr.find_elements(By.TAG_NAME,'td')
  popular_info = {
    "종목명": cols[1].text,
    "검색비율" : cols[2].text,
    "현재가" : cols[3].text,
    "전일비" : cols[4].text,
    "등락률" : cols[5].text,
    "거래량" : cols[6].text,
    "시가" :  cols[7].text,
    "고가" : cols[8].text,
    "저가" : cols[9].text
  }

  popular_data.append(popular_info)

popular_df = pd.DataFrame(popular_data)

# 오늘 날짜 가져오기
today = datetime.datetime.today()

# 시간-분 표시에 :를 사용하게 되면 파일명 인식에 문제가 생겨서, 이런식으로 재조정하게 됨
today = today.strftime('%Y-%m-%d %H-%M')

file_name = f'popular_search_{today}.xlsx'

# xlsx는 csv와 다르게 utf-8 인코딩이 필요없습니다.
popular_df.to_excel(file_name)

print(popular_df)
driver.quit()



