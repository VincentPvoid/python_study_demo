# 使用urllib来获取网页源码
# python中自带urllib，不需要另外安装（但依然需要引入）


# 编码就是将字符串转换成字节码，涉及到字符串的内部表示。
# 解码就是将字节码转换为字符串，将比特位显示成字符。

# 其中decode()与encode()方法可以接收参数，其声明分别为:
# bytes.decode(encoding="utf-8", errors="strict")
# str.encode(encoding="utf-8", errors="strict")



import urllib.request

# 1 定义需要访问的url地址
url = 'http://www.baidu.com'

# 2 模拟浏览器向服务器发送请求
response =  urllib.request.urlopen(url)

# 3 获取返回的响应中页面的源码
# read()方法：返回的是字节形式的二进制数据；
# 为了方便我们阅读，需要将二进制的数据转换为字符串
# 解码：把二进制转换为字符串 decode(需要获取的页面数据的原始编码格式)
# content = response.read()
# content = response.read().decode('utf-8')


# 打印数据
# print(content)



# 方法介绍

# read([num]) 一个一个字节地读取返回的数据；如果有参数，表示读取该数量的字节
# content = response.read()
# content = response.read(10)

# print(response) # <http.client.HTTPResponse object at 0x00000205C7192320>
# 返回的response的类型为HTTPResponse
# print(type(response)) # <class 'http.client.HTTPResponse'>

# readline() 以行为单位读取返回的数据，但只能读取一行
# content = response.readline()

# readlines() 可以按照行的方式把整个文件中的内容进行一次性读取，并且返回的是一个列表，其中每一行为列表的一个元素
# content = response.readlines()

# getcode() 返回状态码 就是xml中的状态码，一般没问题时会返回200
# content = response.getcode()

# geturl() 返回目标的url地址
# content = response.geturl() # http://www.baidu.com

# getheaders() 返回状态信息和响应头等信息
content = response.getheaders() 

print(content)
