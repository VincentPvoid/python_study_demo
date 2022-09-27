import requests
import execjs
from lxml import etree

url = 'https://passport.wanmei.com/sso/login?service=passport'

# response = requests.get(url=url).text
content = requests.get(url=url).text

# print(response)

tree = etree.HTML(content)

pub_key = tree.xpath('//input[@id="e"]/@value')[0]

print(pub_key)

node = execjs.get()
ctx = node.compile(open('./1_ras.js', encoding='UTF-8').read())
# print(type(ctx))
funcStr = 'getPwd("{0}","{1}")'.format('123', pub_key)
pwd = ctx.eval(funcStr)
print(pwd)

