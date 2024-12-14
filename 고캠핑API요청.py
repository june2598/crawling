import requests
import pandas as pd


url = 'http://apis.data.go.kr/B551011/GoCamping/basedList'
serviceKey='UiMBdM3TVt3nZnaqgcg21%2Fuh8GJ%2BasmUct7xQWFs6X%2FiUn2zknKvWeEa%2FJI%2FZlxMO92P9%2BFzFjhp0%2FYOO%2BdB6A%3D%3D'
numOfRows='4703'
pageNo='1'
MobileOS='ETC'
MobileApp='TestApp'
_type='json'

res = requests.get(f'{url}?serviceKey={serviceKey}&numOfRows={numOfRows}&pageNo={pageNo}&MobileOS={MobileOS}&MobileApp={MobileApp}&_type={_type}')
# print(res.status_code)
# print(res.text)
# print(type(res.json()))
# print(res.json())

camping_place_dict = res.json()
print(camping_place_dict['response']['body']['totalCount'])
camping_place_list = camping_place_dict['response']['body']['items']['item']
print(len(camping_place_list))
#
# for camping_place in camping_place_list :
#   print(camping_place['facltNm'])

pd.DataFrame(camping_place_list).to_excel('캠핑정보.xlsx')