from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time

'''
step1) 상품명을 입력받아, 해당 상품의 토론 게시판 첫페이지 글을 스크래핑
'''

url = 'https://finance.naver.com/sise/etf.naver'

# 브라우저 종료 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
driver.implicitly_wait(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

etf_name = input('ETF상품명을 입력하세요: ')


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


for tr in get_post_elements()[4:]:
  cols = tr.find_elements(By.TAG_NAME, "td")
  if len(cols) > 2:
    title_ele = cols[1].find_element(By.TAG_NAME, "a")
    post_date.append(cols[0].text)
    post_title.append(title_ele.get_attribute('title'))
    post_view_count.append(cols[3].text)
    post_empathy.append(cols[4].text)
    post_dislike.append(cols[5].text)
    post_links.append(title_ele.get_attribute('href'))

for post_link in post_links:
  driver.get(post_link)
  time.sleep(2)
  post_soup = BeautifulSoup(driver.page_source, 'html.parser')

  post_contents.append(post_soup.select_one("#body").text.strip())

post_infos = {
  '날짜': post_date,
  '제목': post_title,
  '조회수': post_view_count,
  '공감': post_empathy,
  '비공감': post_dislike,
  '본문': post_contents
}
post_df = pd.DataFrame(post_infos)
print(post_df.head(2))

post_df.to_csv('etf_discussion_posts.csv', index=False, encoding='utf-8-sig')

# 드라이버 종료
driver.quit()





