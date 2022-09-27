# weibo的cookie登录
# 注意：当没有登录（即没有cookie）时，会跳转到登录页面
# 普通页面编码为utf-8，登录页面编码为gb2312；如果编码没有对应上，则会报错


import urllib.request

url = 'https://weibo.cn/chinesehongker'

# headers = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
# }

headers = {
  # ':authority': 'weibo.cn',
  # ':method': 'GET',
  # ':path': '/2008232173/profile',
  # ':scheme': 'https',
  # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  # 'accept-encoding': 'gzip, deflate, br',
  # 'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
  # cookie中一般携带有登录信息；在这个weibo的例子中，有该信息就可以直接访问目标页面，不会跳转到登录页面
  'cookie':' _ttttttt',
  # 进入当前路径的上一个路径；一般用于图片防盗链
  'referer': 'https://weibo.cn/',
  # 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
  # 'sec-ch-ua-mobile': '?0',
  # 'sec-ch-ua-platform': "Windows",
  # 'sec-fetch-dest': 'document',
  # 'sec-fetch-mode': 'navigate',
  # 'sec-fetch-site': 'same-origin',
  # 'sec-fetch-user': '?1',
  # 'upgrade-insecure-requests': 1,
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
}

request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)

# 如果跳转了登录页面，则编码要变为gb2312
# content = response.read().decode('gb2312')

# 如果进入了目标页面，编码为utf-8
content = response.read().decode('utf-8')

# print(content)

# with open('./othersData/weibo.html','w',encoding='gb2312') as fp:
#   fp.write(content)
with open('./othersData/weibo_content.html', 'w', encoding='utf-8') as fp:
  fp.write(content)
