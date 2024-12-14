import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://finance.naver.com/sise/etf.naver'

chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# 특정 요소가 로드될 때까지 대기
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".type_1"))
    )
except Exception as e:
    print("Element not found:", e)

# ETF 테이블의 모든 행(row) 가져오기
rows = driver.find_elements(By.CSS_SELECTOR, ".type_1 tr")  # tr 추가

# rows 리스트의 길이 출력
print(f"Rows count: {len(rows)}")  # Rows의 개수 출력

# 데이터 저장을 위한 리스트 초기화
etf_data = []

# 각 행에서 데이터 추출
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")  # 각 행의 열(column) 가져오기
    if len(cols) >= 7:  # 열의 개수가 7개 이상인지 확인
        etf_info = {
            "종목명": cols[0].text,  # 종목명
            "현재가": cols[1].text,  # 현재가
            "전일비": cols[2].text,  # 전일비
            "등락률": cols[3].text,  # 등락률
            "거래량": cols[5].text,  # 거래량
            "거래대금": cols[6].text  # 거래대금
        }
        etf_data.append(etf_info)

# DataFrame으로 변환
etf_df = pd.DataFrame(etf_data)

# 결과 출력
print(etf_df)

# etf_df.to_csv('etf_data.csv', index=False, encoding='utf-8-sig')

driver.quit()
