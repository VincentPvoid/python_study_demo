# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

import requests
import json

url = 'https://fanyi.baidu.com/sug'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

data = {
  'kw': 'apple'
}

# url 请求资源路径
# data 参数
# kwargs 字典
response = requests.post(url=url, data=data, headers=headers)

content = response.text

# print(content)


# 注意此处不需要encoding参数
# Python 3.9之后，去掉了json.load的encoding参数
# 原因：内部可以自动判断文件编码，无需encoding
obj = json.loads(content)
print(obj)


# 总结
# 1. post请求不需要进行编解码
# 2. post请求参数为data
# 3. 不需要定制请求对象

