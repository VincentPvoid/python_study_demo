import requests
import json
import execjs

url = 'https://sso.kongzhong.com/ajaxLogin?j=j&jsonp=j&service=https://passport.kongzhong.com/&_=1649858933785'

headers = {
  "Referer": "https://passport.kongzhong.com/",
}

response = requests.get(url=url, headers=headers)

# 对返回的字符串进行处理
# 原始KZLoginHandler.jsonpCallbackKongZ({"dc":"AEFAA0CD50F3A9F4A58A052A2939A46B","kzmsg":"","service":"https://passport.kongzhong.com/","state":"0"})
# 要处理为json格式（去头尾不需要的字符）
objStr = response.text.split('KZLoginHandler.jsonpCallbackKongZ(')[1].replace('})','}')

obj = json.loads(objStr)

# print(obj)

dcStr = obj['dc']


node = execjs.get()
ctx = node.compile(open('./1_js_pwd.js', encoding='utf-8').read())
funcName = 'getPwd("{0}","{1}")'.format('123456', dcStr)
pwd = ctx.eval(funcName)
print(pwd)


