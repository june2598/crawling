from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


'''
실시간 인기검색 종목의 간략한 정보를 추출
'''

chrome_option = Options()
chrome_option.add_experimental_option('detach',True)
driver = webdriver.Chrome(options=chrome_option)

url = 'https://finance.naver.com/sise/'

driver.get(url)
driver.implicitly_wait(2)

popular_ul = driver.find_element(By.CSS_SELECTOR,'#popularItemList')

popular_search_data = []

li_list = popular_ul.find_elements(By.TAG_NAME,'li')

for li in li_list:
  item_name = li.find_element(By.CSS_SELECTOR,'a').text
  item_price = li.find_element(By.CSS_SELECTOR,'span').text
  item_condition = li.find_element(By.CSS_SELECTOR,'img').get_attribute('alt')
  popular_search_data.append({
    '종목명': item_name,
    '가격': item_price,
    '상태': item_condition
  })

popular_search_data_df= pd.DataFrame(popular_search_data)
print(popular_search_data_df)

driver.quit()
