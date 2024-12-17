from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import datetime

'''
실시간 업종별 시세 테이블을 가져오는 기능 구현
'''

chrome_option = Options()
chrome_option.add_experimental_option('detach',True)
driver = webdriver.Chrome(options=chrome_option)

url = 'https://finance.naver.com/sise/sise_group.naver?type=upjong'
driver.get(url)
driver.implicitly_wait(2)
soup = BeautifulSoup(driver.page_source,'html.parser')

rows = driver.find_elements(By.CSS_SELECTOR,'.type_1 > tbody:nth-child(3) > tr')

print(f"rows count: {len(rows)}")

sector_data = []

for row in rows:
  cols = row.find_elements(By.TAG_NAME,'td')
  if len(cols) >= 6:
    sector_info = {
      '종목명': cols[0].text,
      '전일비': cols[1].text,
      '전체': cols[2].text,
      '상승': cols[3].text,
      '보합': cols[4].text,
      '하락': cols[5].text,
    }
    sector_data.append(sector_info)

# 그래프 데이터는 selenium 환경에서는 접근할수 없음 -> bs를 통해 따로 접근
graph_spans = soup.select('.type_1 > tbody > tr > td.tc span')
graph_data = [span.text.strip() for span in graph_spans]

# sector_data에 graph_data 추가
for i in range(len(sector_data)):
    if i < len(graph_data):
        sector_data[i]['등락그래프'] = graph_data[i]  # 그래프 데이터를 추가


sector_info_df = pd.DataFrame(sector_data)
print(sector_info_df)

# 오늘 날짜 가져오기
today = datetime.datetime.today()
today = today.strftime('%Y-%m-%d')
new_file_name = f'sector_info_df_{today}.csv'

sector_info_df.to_csv(new_file_name, index=False, encoding='utf-8-sig')

driver.quit()
