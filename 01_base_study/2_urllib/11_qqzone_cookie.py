import urllib.request

url = 'https://user.qzone.qq.com/839576274'

# headers = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
# }

headers = {
  'cookie': 'aaaaaaaaaaaaggggggggg',
  'referer': 'https://qzone.qq.com/',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

request = urllib.request.Request(url = url, headers = headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

# with open('./othersData/qqZone_login.html', 'w', encoding='utf-8') as fp:
#   fp.write(content)

with open('./othersData/qqZone_content.html', 'w', encoding='utf-8') as fp:
  fp.write(content)