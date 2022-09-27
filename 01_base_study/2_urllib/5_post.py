# post请求

import urllib.request
import urllib.parse


url = 'https://fanyi.baidu.com/sug'

data = {
  'kw': 'test'
}

# 把请求的数据转换为对应格式后，还需要编码为字节形式，否则会报错
# data = urllib.parse.urlencode(data)
# encode() 方法以指定的编码格式编码字符串，将其变为字节形式
data = urllib.parse.urlencode(data).encode('utf-8')

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# post请求的参数需要放在请求体中传递
request = urllib.request.Request(url=url, data=data, headers=headers)

response = urllib.request.urlopen(request)

# print(response.read().decode('utf-8'))

content = response.read().decode('utf-8')

# 把字符串转换为json对象
import json
obj = json.loads(content)
print(obj)