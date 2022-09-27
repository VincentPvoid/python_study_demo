import requests
import execjs

# 获取秘钥
url = 'http://login.shikee.com/getkey'

response_text = requests.get(url=url).text
# print(response_text)
pub_key = response_text.split('rsa_n = "')[1].replace('";',"")
# print(pub_key)

node = execjs.get()
ctx = node.compile(open('./1_ras.js', encoding='UTF-8').read())
funcStr = 'getPwd("{0}","{1}")'.format('123456', pub_key)
pwd = ctx.eval(funcStr)
print(pwd)