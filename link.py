import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# ETF 종목탭의 테이블이 ajax 요청으로 js를 통해 불러와지기 떄문에, requests 및 BeautifulSoup만으로 링크를 가져오는데 어려움이 있었습니다.
# 따라서 selenium을 사용해 가져오기로


# 웹 드라이버 설정
driver = webdriver.Chrome()  # Chrome 드라이버 사용
driver.get('https://finance.naver.com/sise/etf.naver')

# 페이지가 로드될 때까지 대기
time.sleep(5)  # 필요에 따라 대기 시간 조정

# ETF 테이블에서 링크 추출
link_elements = driver.find_elements(By.CSS_SELECTOR, '#etfItemTable tr td a')
links = [elem.get_attribute('href') for elem in link_elements]

# 결과 출력
data = {
    'link': links
}

print(data)
df = pd.DataFrame(data, columns=['link'])
print(df)

# 웹 드라이버 종료
driver.quit()