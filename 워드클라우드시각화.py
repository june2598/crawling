import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_excel('주요뉴스기사.xlsx')
# print(df)

# 모든 텍스트를 공백을 구분자로 하여 하나의 문자열로 결합
news_contents_data = df['content'].str.cat(sep= ' ')
# print(news_contents_data)

# 단어 분리:
# news_contents_data.split(): 결합된 문자열을 공백을 기준으로 나누어 문자열을 단어로 분리한 단어 리스트를 생성합니다.
words = news_contents_data.split()
# print(words)

# 단어 빈도수 계산:
# Counter(words): 리스트에 있는 각 단어의 개수를 세어 word_counts라는 Counter 객체를 생성합니다.
word_counts = Counter(words)
# print(word_counts)

# 단어 구름 생성:
#
#  WordCloud(...): 단어 구름을 생성할 때 사용할 다양한 옵션을 설정합니다.
#    width: 단어 구름의 너비.
#    height: 단어 구름의 높이.
#    background_color: 배경색.
#    font_path: 사용할 폰트의 경로 (한국어 지원을 위해 Malgun Gothic 사용).
#    .generate_from_frequencies(word_counts): 단어의 빈도수에 따라 단어 구름을 생성합니다.
wordcloud = WordCloud(width=800,height=400,background_color='white',\
                      font_path='c:/Windows/Fonts/malgun.ttf')\
  .generate_from_frequencies(word_counts)

# 단어 구름 시각화 준비:
  # plt.figure(figsize=(10, 5)): 시각화할 그림의 크기를 설정합니다.
  # plt.imshow(wordcloud, interpolation='bilinear'): 생성한 단어 구름 이미지를 화면에 표시합니다.

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')

# 축 제거 및 표시:
  # plt.axis('off'): 축을 제거하여 깔끔하게 표시합니다.
  # plt.show(): 최종적으로 생성된 단어 구름을 화면에 출력합니다.

plt.axis('off')  # 축 제거
plt.show()