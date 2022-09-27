import sys
sys.path.append("D:\Python\Python310\Lib\site-packages")

import requests

url = 'http://www.baidu.com'

response = requests.get(url=url)

# 一个类型和六个属性

# Response类型
# print(type(response)) # <class 'requests.models.Response'>

# 设置响应的编码格式
# response.encoding = 'utf-8'

# 以字符串的形式返回网页源码
# print(response.text)

# 获取请求的url地址
# print(response.url)

# 以二进制字节的形式返回网页源码
# print(response.content)

# 返回响应的状态码
# print(response.status_code)

# 返回响应头
print(response.headers)
