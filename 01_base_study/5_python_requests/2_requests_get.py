# urllib
# 1. 一个类型和六个方法
# 2. get请求
# 3. post请求
# 4. ajax的get请求
# 5. ajax的post请求
# 6. cookie登录
# 7. 代理

# requests
# 1. 一个类型和六个属性
# 2. get请求
# 3. post请求
# 4. 代理
# 5. cookie登录



# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

import requests

# 注意：这里的?可写可不写
# url = 'https://www.baidu.com/s?'
url = 'https://www.baidu.com/s'

data = {
  'wd':'血源诅咒'
}

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# url 请求资源路径
# params 参数
# kwargs 字典
response = requests.get(url=url, params=data, headers=headers)

content = response.text

print(content)


# 总结
# 1. 参数使用params传递，以字典（对象）的方式传递
# 2. 参数不需要使用urlencode编码
# 3. 不需要定制请求对象
# 4. 请求资源路径（url）中的?可写可不写

