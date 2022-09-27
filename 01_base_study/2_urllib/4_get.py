# get请求

import urllib.request
import urllib.parse


# # 请求目标的url地址需要转换为unicode编码，否则会报错
# # 报错 无法将“url”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。请检查名称的拼写，如果包括路径，请确保路径正确，然后再试一次。
# # url = 'https://www.baidu.com/s?wd=血源诅咒'


# # 可以使用urllib.parse.quote()进行编码的转换
# url = 'https://www.baidu.com/s?wd='
# searchKeyWord = urllib.parse.quote('血源诅咒')

# # print(searchKeyWord)
# url += searchKeyWord
# # print(url)

# # 设置UA
# headers = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
# }

# # 解决反爬的其中一种方法：定制请求对象
# request = urllib.request.Request(url=url, headers=headers)

# # 模拟浏览器向服务器发送请求
# response = urllib.request.urlopen(request)

# # 获取响应内容（二进制），转换为utf-8编码内容
# content = response.read().decode('utf-8')

# print(content)



# 如果有多个请求参数，可以使用urllib.parse.urlencode()方法进行转码

BASE_URL = 'https://www.baidu.com/s?'

data = {
  'wd':'血源诅咒',
  'year': '2016',
  'conpany':'From Software'
}

# 把data转换为key1=value1&key2=value2...这种形式
data = urllib.parse.urlencode(data)
print(data)

# 请求资源路径
url = BASE_URL + data
# print(url)

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)

print(response.read().decode('utf-8'))