import requests
import execjs

# 获取秘钥
url = 'https://store.steampowered.com/login/getrsakey/'
data = {
  'donotcache': 1648559830921,
  'username': 'abc'
}

response_obj = requests.post(url=url, data=data).json()
print(response_obj)
mod = response_obj['publickey_mod']
exp = response_obj['publickey_exp']

# 执行js函数，生成密码
node = execjs.get()
ctx = node.compile(open('./1_login.js',encoding='utf-8').read())
funcName = 'getSteamPwd("{0}", "{1}", "{2}")'.format('123', mod, exp)
pwd = ctx.eval(funcName)
print(pwd)
