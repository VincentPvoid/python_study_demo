import urllib.request

url = 'http://ip111.cn/'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

request = urllib.request.Request(url=url, headers=headers)

proxies = {
  'http': '109.201.9.100:8080'
}

handler = urllib.request.ProxyHandler(proxies=proxies)

opener = urllib.request.build_opener(handler)

response = opener.open(request)

content = response.read().decode('utf-8')

with open('./othersData/_ip.html','w',encoding='utf-8') as fp:
  fp.write(content)