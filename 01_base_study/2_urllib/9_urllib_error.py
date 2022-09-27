# 异常

import urllib.request

# url = 'https://blog.csdn.net/heqiang525/article/details/89879056'

# 访问错误的地址；urllib.error.HTTPError错误
# url = 'https://blog.csdn.net/heqiang525/article/details/898790561'

# 访问不存在的域名 urllib.error.URLError错误
url = 'https://www.notexistedsite111111.com'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

try:
  request = urllib.request.Request(url=url, headers=headers)

  response = urllib.request.urlopen(request)

  content = response.read().decode('utf-8')

  print(content)
except urllib.error.HTTPError:
  print('system is updating...')
except urllib.error.URLError:
  print('wrong url')