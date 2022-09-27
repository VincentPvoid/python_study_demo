import requests
import time
import random
import execjs

# python时间戳*1000 = js时间戳
# int用于去掉时间后面的小数
lts = str(int(time.time() *1000))

# 时间戳+1位随机整数
salt = lts + str(int(random.random() * 10))


# print(lts)
# print(salt)
word = input('please input word: ')

node = execjs.get()
ctx = node.compile(open('./1_md5.js', encoding='utf-8').read())
funcName = 'getSign("{0}","{1}")'.format(word, salt)
sign = ctx.eval(funcName)
# print(sign)


url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
  'Referer': 'https://fanyi.youdao.com/',
  'Cookie': '',
}


data = {
  'i': word,
  'from': 'AUTO',
  'to': 'AUTO',
  'smartresult': 'dict',
  'client': 'fanyideskweb',
  'salt': salt,
  'sign': sign,
  'lts': lts,
  'bv': 'ac3968199d18b7367b2479d1f4938ac2',
  'doctype': 'json',
  'version': '2.1',
  'keyfrom': 'fanyi.web',
  'action': 'FY_BY_REALTlME',
}

response = requests.post(url = url, headers=headers, data=data).json()

print(response)


