# 例：jsonpath解析淘票票

import sys
sys.path.append("D:\Python\Python310\Lib\site-packages")

import urllib.request

url = 'https://dianying.taobao.com/cityAction.json'
headers = {
  'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
  # 'accept-encoding': 'gzip, deflate, br',
  # 'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
  'cookie': 'grgers',
  'referer':' https://dianying.taobao.com/',
  # 'sec-ch-ua': '"Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
  # 'sec-ch-ua-mobile': '?0',
  # 'sec-ch-ua-platform': "Windows",
  # 'sec-fetch-dest': 'empty',
  # 'sec-fetch-mode': 'cors',
  # 'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}

request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

content = content.split('(')[1].split(')')[0]

# print(content)

with open('./testData/taopiaopiao_cities.json','w', encoding='utf-8') as fp:
  fp.write(content)


import json
import jsonpath

obj = json.load(open('./testData/taopiaopiao_cities.json', 'r', encoding='utf-8'))

region_list = jsonpath.jsonpath(obj, '$..regionName')

print(region_list)