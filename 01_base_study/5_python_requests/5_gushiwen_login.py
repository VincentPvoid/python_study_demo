# 例：登录古诗文网

# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

import requests
from bs4 import BeautifulSoup

# 登录时需要的参数
# __VIEWSTATE: JlGg1gZ2tOxDlw2zyzHYE66aTlGE5GqmGh3GNwLGmBGGHwrA6L766auEBVwgJjhvBFgU17d3B3RIRkBKAOMfMOARK+mvtrpyEj6WjMW/3pMFA+reipGBiHtfS08=
# __VIEWSTATEGENERATOR: C93BE1AE
# from: http://so.gushiwen.cn/user/collect.aspx
# email: sldfjls@345.com
# pwd: rgtjtjg
# code: LEZE
# denglu: 登录

# 登录页面地址
url = 'https://so.gushiwen.cn/user/login.aspx'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# 获取登录页面源码
response = requests.get(url=url, headers=headers)

content = response.text

# print(content)


# 解析页面源码，获取 __VIEWSTATE 和 __VIEWSTATEGENERATOR 的value
soup = BeautifulSoup(content, 'lxml')

__VIEWSTATE_value = soup.select('#__VIEWSTATE')[0].attrs.get('value')
__VIEWSTATEGENERATOR_value = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')

# print(__VIEWSTATE_value)
# print(__VIEWSTATEGENERATOR_value)


BASU_URL = 'https://so.gushiwen.cn/'
# 获取图片url；需要进行拼接
img_url = BASU_URL + soup.select('#imgCode')[0].attrs.get('src')
# print(img_url)

# 获取到验证码图片后下载到本地，手动输入验证码的值，进行登录
# 注意：不能使用urllib.request.urlretrieve进行下载；
# 因为使用该方法是重新发起一个请求，与当前登录请求不是同一个，因此验证码会不对应
# import urllib.request
# urllib.request.urlretrieve(url=img_url, filename='code.jpg')


# 因此需要使用requests.session()方法
# requests.session():维持会话,可以让我们在跨请求时保存某些参数
# 注意：新版requests中该方法改为了requests.Session()
session = requests.Session()
response_code = session.get(img_url)
# 需要把图片保存为文件，因此需要以二进制字节的形式返回
content_code = response_code.content
# wb表示把二进制数据写入到文件
with open('code.jpg', 'wb') as fp:
  fp.write(content_code)

# 输入图片中的验证码
code_value = input('please input Verification Code: ')

data = {
  '__VIEWSTATE' : __VIEWSTATE_value,
  '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR_value,
  'from': 'http://so.gushiwen.cn/user/collect.aspx',
  'email': 'wulgtgxgyp@iubridge.com',
  'pwd' : '123123',
  'code':code_value,
  'denglu': '登录',
}

response_post = session.post(url=url, headers=headers, data = data)

content_post = response_post.text

with open('gushiwen.html', 'w',encoding='utf-8') as fp:
  fp.write(content_post)



# 难点
# 1. 隐藏参数的获取
# 2. 在同一个请求中获取验证码（使用requests.Session()方法保持会话）