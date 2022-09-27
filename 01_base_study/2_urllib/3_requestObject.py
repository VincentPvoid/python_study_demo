# 请求对象的定制

# url的组成
# https://www.baidu.com/s?wd=test

# http/https    www.baidu.com     80/443     s      wd=test    #
#  协议           主机            端口号    路径      参数    锚点

# http    80
# https   443
# mysql   3306
# oracle  1521
# redis   6379
# mongodb 27017

import urllib.request

url = 'https://www.baidu.com'

# 无法直接访问该url，目标地址使用了UA反爬；因此需要设置UA代理
# 使用urlopen()方法无法传递header对象，因此需要用其他方法
# response = urllib.request.urlopen(url)

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# 注意；因为Request()方法参数设定的问题，如果直接传递这两个参数位置无法对应，因此要写成 形参=实参 的形式
request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)

content = response.read().decode('utf-8')

print(content)