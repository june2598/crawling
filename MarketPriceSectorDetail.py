# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
# import datetime


sector_df = pd.read_csv('sector_info_df_2024-12-18.csv')

def sector_detail_url(sector_name):
  '''
  업종명으로 해당업종의 상세목록을 볼수있는 url을 반환하는 함수
  :param sector_name: 업종명
  :return: 해당업종명에 해당하는 종목리스트를 볼수있는 주소
  '''
  sector_code = sector_df[sector_df['업종명'] == sector_name]['업종코드'].values[0]
  if sector_code.size == 0:
    print('존재하지 않는 업종입니다.')
    return None
  print(type(sector_code))      #numpy.int64
  url = f'https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no={sector_code}'
  return url

name = input('찾고자하는 업종명을 선택하세요. : ')

request_url = sector_detail_url(name)
if request_url is None:
  exit()

print(request_url)

'''
처음에는 selenium을 사용해서 스크래핑을 시도하였습니다.
그러나 퍼포먼스나 서버 부하적 측면에서, BeautifulSoup를 사용할 수 있으면 selenium 사용을 최소화 하는것이 좋다 판단했습니다.
따라서 selenium을 사용한 부분을 주석처리하고, BeautifulSoup를 사용해 직접 파싱하는 방식을 채택했습니다.
이 변경으로 퍼포먼스가 상승할것을 기대 할 수 있다고 생각합니다.

'''

# url = 'https://finance.naver.com/item/main.naver?code=305540'
# res = requests.get(url)
# print(res.status_code)
#
# soup = BeautifulSoup(res.content,'lxml')
# element_list = soup.select('.tb_type1_a > tbody:nth-child(2) tr')

res = requests.get(request_url)
if res.status_code != 200:
  print('데이터를 가져오는 데 실패했습니다.')
  exit()
print(res.status_code)

soup = BeautifulSoup(res.content,'html.parser')

# chrome_option=Options()
# chrome_option.add_experimental_option('detach',True)
# driver = webdriver.Chrome(options=chrome_option)
#
# driver.get(request_url)

rows = soup.select('#contentarea > div:nth-child(5) > table > tbody > tr')

stock_list = []

for tr in rows :
  cols = tr.find_all("td")                        # BeautifulSoup 환경
  # cols = tr.find_elements(By.TAG_NAME, "td")    # Selenium 환경
  if len(cols) >= 9:
    # 종목명뒤에 *가 붙은 종목은 코스닥 종목임을 파악했습니다.
    # 데이터 활용을위해, 종목명에서 *를 제거하면서 *이 있는 종목과 없는종목을 구분하기위해 새 column을 추가했습니다.

    stock_name = cols[0].text.strip()
    is_kosdaq = '*' in stock_name  # 별표가 있으면 True, 없으면 False
    stock_info = {
    '종목명':stock_name.replace('*', '').strip(),  # * 기호 제거
    '현재가':cols[1].text,
    '전일비':cols[2].find(class_='tah').text.strip(),
    # '전일비': cols[2].find_element(By.CLASS_NAME, 'tah').text,   # Selenium 환경
    'UpDown':cols[2].find(class_='blind').text.strip(),
    # 'UpDown': cols[2].find_element(By.CLASS_NAME, 'blind').text,    # Selenium 환경
    '등락률':cols[3].text,
    '매수호가':cols[4].text,
    '매도호가':cols[5].text,
    '거래량':cols[6].text,
    '거래대금':cols[7].text,
    '전일거래량':cols[8].text,
    '코스닥 여부': is_kosdaq  # 코스닥 여부 추가

    }
    stock_list.append(stock_info)


stock_list_df = pd.DataFrame(stock_list)
# stock_list_df.to_excel('stock_list_df_soup.xlsx')

print(stock_list_df.head())






