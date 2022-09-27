# 百度详细翻译案例

import urllib.request
import urllib.parse

url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'

data = {
  'from': 'en',
  'to': 'zh',
  'query': 'spider',
  'transtype': 'realtime',
  'simple_means_flag': 3,
  'sign': '63766.268839',
  'token': 'gggggggggggggggggggggggggggggg',
  'domain': 'common',
}

data = urllib.parse.urlencode(data).encode('utf-8')

headers = {
  # 'Accept':' */*',
  # 'Accept-Encoding':' gzip, deflate, br,', # 设置接收的编码格式；这里如果设置了，获得响应后会因为编码格式不对而报错（如果不转码则不会报错）
  # 'Accept-Language': 'zh-CN,zh;q=0.9',
  # 'Connection': 'keep-alive',
  # 'Content-Length': '136',
  # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  # # 该案例实际需要的是Cookie这个参数；其他都可以不设置
  'Cookie': 'yjtyjtyjtyjtj',
  # 'Host': 'fanyi.baidu.com',
  # 'Origin': 'https://fanyi.baidu.com',
  # 'Referer': 'https://fanyi.baidu.com/',
  # 'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
  # 'sec-ch-ua-mobile': '?0',
  # 'sec-ch-ua-platform': "Windows",
  # 'Sec-Fetch-Dest': 'empty',
  # 'Sec-Fetch-Mode': 'cors',
  # 'Sec-Fetch-Site': 'same-origin',
  # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
  # 'X-Requested-With': 'XMLHttpRequest',
}

request = urllib.request.Request(url=url, data=data, headers=headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

import json

print(json.loads(content))