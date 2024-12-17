from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

'''
final)
ETF상품명, 시작일, 종료일을 입력받아 해당 종목의 종목 토론방 게시글을 스크래핑하는 기능 구현
페이징을 고려해 페이징을 이동하면서 스크래핑 하는 기능까지 구현
클린봇이 필터링 한 게시글로 인한 충돌의 해결
각종예외 상황처리, 대기시간 설정등 미세조정
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
start_date = input('시작일을 입력하세요 (YYYY.MM.DD): ')
end_date = input('종료일을 입력하세요 (YYYY.MM.DD): ')

detail_url = 'https://finance.naver.com' + soup.select_one('#etfItemTable').find('a', string=etf_name).attrs['href']

# 토론실 링크 주소 가져오기
discussion_bbs_url = detail_url.replace('main', 'board')

# 날짜 형식 변환
start_date = pd.to_datetime(start_date, format='%Y.%m.%d')
end_date = pd.to_datetime(end_date, format='%Y.%m.%d')

post_links = []
post_date = []
post_title = []
post_view_count = []
post_empathy = []
post_dislike = []
post_contents = []

# 페이지 번호 초기화
page_number = 1
stop = False

# 페이지 순환을 위한 반복
while not stop:

  # 현재 페이지 주소
  current_page_url = f"{discussion_bbs_url}&page={page_number}"
  driver.get(current_page_url)

  # 로드가 다 될때까지 대기시간 설정
  WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div.section.inner_sub > table.type2 > tbody > tr')))

  # 게시글 요소 가져오기
  trs = driver.find_elements(By.CSS_SELECTOR, '#content > div.section.inner_sub > table.type2 > tbody > tr')

  if len(trs) <= 4:  # 게시글이 없는 경우 종료
    print("더 이상 게시글이 없습니다.")
    stop = True
    break

  # td 요소가 6개인 trs 필터링
  post_rows = [tr for tr in trs if len(tr.find_elements(By.TAG_NAME, 'td')) == 6]

  for tr in post_rows:
    cols = tr.find_elements(By.TAG_NAME, "td")

    # 2024-12-17 추가 : '클린봇이 이용자 보호를 위해 숨긴 게시글입니다.' 게시글의 경우 td 안에 a 태그가 없기때문에, 이 조건으로 거르기 전에는 에러가 발생했었음
    if len(cols[1].find_elements(By.TAG_NAME, "a")) > 0:                        # 2024-12-17 추가한 조건
      title_ele = cols[1].find_element(By.TAG_NAME, "a")
      # 날짜 추출 (YYYY.MM.DD HH:MM)
      post_date_str = cols[0].text.strip()
      # 문자열을 날짜 타입으로 변경
      post_date_obj = pd.to_datetime(post_date_str, format='%Y.%m.%d %H:%M')

      # 날짜 필터링
      if start_date <= post_date_obj <= end_date:
        post_date.append(post_date_str)                         # 날짜
        post_title.append(title_ele.get_attribute('title'))     # 게시글 제목
        post_view_count.append(cols[3].text.strip())            # 조회수
        post_empathy.append(cols[4].text.strip())               # 공감
        post_dislike.append(cols[5].text.strip())               # 비공감
        post_links.append(title_ele.get_attribute('href'))      # 게시글 본문을 찾기위한 링크

    else:           # td가 정상적으로 6개 존재하지만 a태그가 없는 tr -> 클린봇이 차단한 게시글이라는 것을 파악함
      continue

  # 마지막 게시글의 작성날짜 확인
  last_post_date_str = post_rows[-1].find_elements(By.TAG_NAME, "td")[0].text.strip()
  last_post_date_obj = pd.to_datetime(last_post_date_str, format='%Y.%m.%d %H:%M')

  # 현재 페이지가 마지막 페이지 인지 확인
  try:
    # 마지막 페이지 에서는 맨끝 버튼이 없는 점을 이용
    driver.find_element(By.CSS_SELECTOR,
                        '#content > div.section.inner_sub > table.tbl_pagination > tbody > tr > td:nth-child(2) > table > tbody > tr > td.pgRR')
    # 마지막 페이지가 아닐 경우, 시작일 보다 현재 페이지의 마지막 글 작성 날짜가 미래 라면, 페이지 +1
    if start_date <= last_post_date_obj:
      page_number += 1
    else:
      stop = True
  except NoSuchElementException:
    # 마지막 페이지인 경우
    print("현재 페이지가 마지막 페이지 입니다.")
    stop = True
  except Exception as e:
    # 다른 예외가 발생한 경우
    print(f"예상치 못한 오류 발생: {e}")

# 게시글 본문 수집
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

# post_df.to_excel('etf_discussion_posts.xlsx', index=False, encoding='utf-8-sig')

# 드라이버 종료
driver.quit()