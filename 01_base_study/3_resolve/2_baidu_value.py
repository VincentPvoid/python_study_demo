# 例子 获取百度首页 百度一下 值

# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

from lxml import etree

import urllib.request

url = 'https://www.baidu.com'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)

# 获取网页源码
content = response.read().decode('utf-8')

# print(content)

# 解析服务器响应的数据
tree = etree.HTML(content)

# 获取需要的数据（注意在该例子中获取的是input的值，因此需要用value来获取）
res = tree.xpath("//input[@id='su']/@value")

print(res)

