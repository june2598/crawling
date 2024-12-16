from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time
from datetime import datetime


url = 'https://finance.naver.com/sise/etf.naver'

# 브라우저 종료 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
driver.implicitly_wait(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

etf_name = input('ETF상품명을 입력하세요: ')
start_date = input('시작일을 입력하세요 (YYYY.MM.DD): ')
end_date = input('종료일을 입력하세요 (YYYY.MM.DD): ')


detail_url = 'https://finance.naver.com' + soup.select_one('#etfItemTable').find('a', string=etf_name).attrs['href']

# 토론실 링크 주소 가져오기
discussion_bbs_url = detail_url.replace('main', 'board')
driver.get(discussion_bbs_url)


def get_post_elements():
  trs = driver.find_elements(By.CSS_SELECTOR,'#content > div.section.inner_sub > table.type2 > tbody > tr')
  return trs

post_links = []
post_date = []
post_title = []
post_view_count=[]
post_empathy=[]
post_dislike=[]
post_contents=[]

# 날짜 형식 변환
start_date = datetime.strptime(start_date, '%Y.%m.%d')
end_date = datetime.strptime(end_date, '%Y.%m.%d')


for tr in get_post_elements()[4:]:
  cols = tr.find_elements(By.TAG_NAME, "td")
  if len(cols) > 2:
    title_ele = cols[1].find_element(By.TAG_NAME, "a")

    #날짜 추출 (YYYY.MM.DD HH:MM)
    post_date_str = cols[0].text.strip()

    # 날짜 형식을 YYYY.MM.DD HH:MM로 변환
    post_date_obj = datetime.strptime(post_date_str, '%Y.%m.%d %H:%M')

    # 날짜 구간 필터링 :
    if start_date <= post_date_obj <= end_date:
      post_date.append(post_date_str)
      post_title.append(title_ele.get_attribute('title'))
      post_view_count.append(cols[3].text.strip())
      post_empathy.append(cols[4].text.strip())
      post_dislike.append(cols[5].text.strip())
      post_links.append(title_ele.get_attribute('href'))

# 게시글 본문 가져오기
for post_link in post_links:
  driver.get(post_link)
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#body")))
  post_soup = BeautifulSoup(driver.page_source, 'html.parser')

  # 본문 내용 정리
  body_content = post_soup.select_one("#body")
  if body_content:
    post_contents.append(body_content.text.strip().replace('\n', ' '))
  else:
    post_contents.append("본문 없음")

post_infos = {
  '날짜': post_date,
  '제목': post_title,
  '조회수': post_view_count,
  '공감': post_empathy,
  '비공감': post_dislike,
  '본문': post_contents
}
post_df = pd.DataFrame(post_infos)
print(post_df)

post_df.to_excel('etf_discussion_posts.xlsx', index=False, encoding='utf-8-sig')

# 드라이버 종료
driver.quit()





