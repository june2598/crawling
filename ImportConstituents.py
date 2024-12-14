import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#TIGER 2차전지 테마주
url = 'https://finance.naver.com/item/main.naver?code=305540'
res = requests.get(url)
print(res.status_code)

soup = BeautifulSoup(res.content,'lxml')
element_list = soup.select('.tb_type1_a > tbody:nth-child(2) tr')
# print(element_list)

data = []
for ele in element_list :
  row_data = {}
  link = ele.select_one('a[href]')
  proportion = ele.select_one('.per')
  fluctuationRate = ele.select('em.f_down, em.f_up')
  number_of_share = ele.select_one('td:nth-of-type(2)')  # 4번째 td 요소
  price = ele.select_one('td:nth-of-type(4)')  # 4번째 td 요소
  previous_close = ele.select_one('td:nth-of-type(5)')  # 5번째 td 요소

  #구성족목명 및 링크
  if link:
    row_data['구성종목'] = link.text
    row_data['link'] = link.attrs.get('href')

  if number_of_share:
    row_data['주식수'] = number_of_share.text

  #구성비중
  if proportion:
    # 비율만 가져오기위해 정규표현식을 사용함
    #\d+는 하나 이상의 숫자를 의미합니다.(\.\d+)?는 소수점 이하 숫자가 있을 경우를 처리합니다. %는 퍼센트 기호
    match = re.search(r'(\d+(\.\d+)?%)', proportion.text)
    if match:
      row_data['구성비중'] = match.group(0)
  # 시세
  if price:
    row_data['시세'] = price.text

  #전일비
  if previous_close:
    row_data['전일비'] = previous_close.text

  #등락률
  for rate in fluctuationRate:
    match = re.search(r'([+\-]\d+(\.\d+)?%)', rate.text)
    if match:
      row_data['등락률'] = match.group(0)

  if row_data:
    data.append(row_data)

# Pandas DataFrame으로 변환
df = pd.DataFrame(data)
# 열 순서 조정

df = df[['구성종목', 'link', '주식수', '구성비중', '시세', '전일비', '등락률']]

# 1. 공백 및 특수 문자 제거 (\n, \t 부분)
df = df.apply(lambda x: x.str.replace(r'\s+', ' ', regex=True).str.strip() if x.dtype == "object" else x)

# 공백 또는 NaN으로 이루어진 행 제거
df = df[~df.apply(lambda x: (x.isna() | (x == '')).all(), axis=1)]

# 공백 또는 NaN으로 이루어진 열 제거
df = df.loc[:, ~df.isna().all(axis=0) & ~(df == '').all(axis=0)]

# 결과를 엑셀 파일로 저장
df.to_excel('주요구성자산.xlsx', index=False)

# 결과 출력
print(df)
