# http 요청 응답, html 구문 분석
import requests
from bs4 import BeautifulSoup
import re

# 셀레니움 브라우저의 동작을 자동화하는 패키지
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 데이터 분석 패키지
import pandas as pd

import datetime


url = 'https://finance.naver.com/sise/etf.naver'

# # 브라우저 종료 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option('detach',True)

# # 웹 드라이버를 이용한 브라우저 제어
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
driver.implicitly_wait(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

etf_name = input('ETF상품명을 입력하세요')
print(etf_name)

detail_url = 'https://finance.naver.com' + soup.select_one('#etfItemTable').find('a',string=etf_name).attrs['href']
driver.get(detail_url)


trs = driver.find_elements(By.CSS_SELECTOR,'#content > div.section.etf_asset > table > tbody > tr')
filtered_rows = []

for tr in trs[1:]:
  # tr 내의 모든 td 요소 찾기
  tds = tr.find_elements(By.CSS_SELECTOR, 'td')

  # 'blank' 클래스가 포함된 td가 있거나, td가 없거나, 클래스명이 'division_line'인 td가 존재하는 경우 제외
  if all('blank' not in td.get_attribute('class') and
         'division_line' not in td.get_attribute('class') for td in tds):
    # print([td.text for td in tr.find_elements(By.CSS_SELECTOR,'td')])

    filtered_rows.append([td.text for td in tr.find_elements(By.CSS_SELECTOR, 'td')])

# print(len(filtered_rows))
# print(filtered_rows)

columns = [td.text for td in trs[0].find_elements(By.CSS_SELECTOR,'th')]

df = pd.DataFrame(filtered_rows,columns=columns)

print(df)

# 오늘 날짜 가져오기
today = datetime.datetime.today()
today = today.strftime('%Y-%m-%d')
new_file_name = f'주요구성자산_{etf_name}_{today}.xlsx'

df.to_excel(new_file_name, index=False)

driver.quit()