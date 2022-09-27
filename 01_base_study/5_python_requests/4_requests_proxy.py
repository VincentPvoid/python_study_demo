# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

import requests

url = 'http://www.baidu.com/s?'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

data = {
  'wd':'ip'
}
proxy = {
  'http': '189.165.50.0:10101'
}

response = requests.get(url = url, headers=headers, params=data, proxies=proxy)

content = response.text

with open('test_ip.html', 'w', encoding='utf-8') as fp:
  fp.write(content)