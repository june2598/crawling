import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL 설정
url = 'https://finance.naver.com/item/main.naver?code=305540'

# Chrome 드라이버 설정
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

# 특정 요소가 로드될 때까지 대기
WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.CSS_SELECTOR, '.tb_type1_a > tbody > tr'))
)

# 데이터 저장을 위한 리스트 초기화
data = []

# 데이터 추출
rows = driver.find_elements(By.CSS_SELECTOR, '.tb_type1_a > tbody > tr')
for row in rows:
  row_data = {}

  try:
    link = row.find_element(By.CSS_SELECTOR, 'a[href]')
    row_data['구성종목'] = link.text
    row_data['link'] = "https://finance.naver.com" + link.get_attribute('href')  # 절대 경로로 변환
  except Exception as e:
    print("구성종목 링크를 찾는 중 오류 발생:", e)

  try:
    number_of_share = row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(2)')
    row_data['주식수'] = number_of_share.text
  except Exception as e:
    print("주식수 정보를 찾는 중 오류 발생:", e)

  try:
    proportion = row.find_element(By.CSS_SELECTOR, '.per')
    row_data['구성비중'] = proportion.text.strip()
  except Exception as e:
    print("구성비중 정보를 찾는 중 오류 발생:", e)

  try:
    price = row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(4)')
    row_data['시세'] = price.text.strip()
  except Exception as e:
    print("시세 정보를 찾는 중 오류 발생:", e)

  try:
    previous_close = row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(5)')
    row_data['전일비'] = previous_close.text.strip()
  except Exception as e:
    print("전일비 정보를 찾는 중 오류 발생:", e)

  try:
    fluctuationRate = row.find_elements(By.CSS_SELECTOR, 'em.f_down, em.f_up')
    for rate in fluctuationRate:
      row_data['등락률'] = rate.text.strip()
  except Exception as e:
    print("등락률 정보를 찾는 중 오류 발생:", e)

  if row_data:
    data.append(row_data)

# Pandas DataFrame으로 변환
df = pd.DataFrame(data)

# 1. 공백 및 특수 문자 제거 (\n, \t 부분)
df = df.apply(lambda x: x.str.replace(r'\s+', ' ', regex=True).str.strip() if x.dtype == "object" else x)

# 공백 또는 NaN으로 이루어진 행 제거
df = df[~df.apply(lambda x: (x.isna() | (x == '')).all(), axis=1)]

# 공백 또는 NaN으로 이루어진 열 제거
df = df.loc[:, ~df.isna().all(axis=0) & ~(df == '').all(axis=0)]

df = df.dropna()

# 결과를 엑셀 파일로 저장
df.to_excel('주요구성자산2.xlsx', index=False)

# 결과 출력
print(df)

# 드라이버 종료
driver.quit()