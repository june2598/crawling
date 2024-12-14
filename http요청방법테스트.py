# http 요청받고, 요청하는
import requests

# print(dir(requests))
res = requests.get('https://python.org')
# print(res)
# print(type(res))
# print(dir(res))

# 응답 본문의 문자열 인코딩을 자동 감지하여 인코딩된 데이터를 반환
# print(res.text)
# 응답 본문을 인코딩 변환 없이 원시 바이트 데이터를 그대로 반환
print(res.content)

# requests.post('https://python.org', json={'name':'hongildong'})

# html을 해석할수 있는 Parser
