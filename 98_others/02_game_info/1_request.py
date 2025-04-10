import requests
# from lxml import etree
from bs4 import BeautifulSoup
from dateutil import parser
import re

def saveHtml(file_name, file_content):
 # 注意windows文件命名的禁用符，比如 /
 with open(file_name.replace('/', '_') + ".html", "w", encoding='utf-8') as f:
  f.write(file_content)

# 日期格式转换 转换为YYYY-MM-DD这种格式
def format_date(date_str):
  datetime_struct = parser.parse(date_str)
  return datetime_struct.strftime('%Y-%m-%d')

# 下载图片
def dl_img(url):
  res = requests.get(url)
  with open('header.jpg', mode="wb") as fp:
    fp.write(res.content)

# 获取开发商字符串
def get_dev_str(list):
  developers = ''
  for i in range(len(list)):
    #  print(list[i].get_text())
    developers += list[i].get_text()
    if(i < len(list) - 1):
      developers += ','
  return developers

# 获取标签字符串，默认最多5个
def get_tags_str(list, max_num = 5):
  tags = ''
  length = max_num
  if(len(list) < length):
    length = len(list)
  for i in range(length):
    #  print(list[i].get_text())
    tags += list[i].get_text().strip()
    if(i < length - 1):
      tags += ','
  return tags


# url = 'https://store.steampowered.com/app/2292030/'
url = input('target steam url: ')

proxy = {'https': 'http://127.0.0.1:7890', 'http': 'http://127.0.0.1:7890'}

response = requests.get(url=url, proxies=proxy)

content = response.text
# print(content)

# saveHtml('test', content)
# tree = etree.HTML(content)

# # 标题
# title = tree.xpath('//div[@id="appHubAppName"]/text()')
# # 描述
# description = tree.xpath('//div[@class="game_description_snippet"]/text()')
# # 日期
# date = tree.xpath('//div[@class="date"]/text()')
# # 开发商
# developers = tree.xpath('//div[@id="developers_list"]/a')
# 发行商 此处第一个选出的为开发商字段，要取后面第二项的字段
# publishers = tree.xpath('//div[@class="dev_row"]/div[contains(@class, "summary")]/a')
# print(date)


soup = BeautifulSoup(content, 'lxml')

# 标题
title = soup.select('#appHubAppName')[0].get_text()
# 描述
description = soup.select('.game_description_snippet')[0].get_text().strip()
# 日期；如果未定获取到的字符串为To be announced 或 Coming soon
date = soup.select('.date')[0].get_text()
# print(date)
# if(date.startswith("To") or date.startswith("Coming")):
#   date = "未定"
# else:
#   date = format_date(date)
try:
  date = format_date(date)
except:
  date = "未定"
# print(title, description, date)
developers_a_list = soup.select('#developers_list a')
publishers_a_list = soup.select('.dev_row .summary a')
# //div[contains(@class, "popular_tags")]/a
tags_list = soup.select('.popular_tags a')
# document.querySelectorAll('.details_block .linkbar')[0]
# link = soup.select('.details_block .linkbar')[0].attrs['href']
link = soup.select('.details_block .linkbar')[0].attrs['href'].replace('%2F','/').replace('%3A', ':')
# print(link)

# 获取图片url
# https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/xxxxxx/ed75864714bc842ce9980cdc7980e7151da3ff35/header.jpg?t=1742324437
# https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/xxxxxx/header.jpg?t=1743192679
# reg_img_prefix = re.compile('https://shared.[^\.]+.steamstatic.com/store_item_assets/steam/apps/[0-9]+/')
# img_src = soup.select('.game_header_image_full')[0].attrs['src'].replace('header','library_600x900')

# 获取图片地址，并去除后面的时间参数 ?=xxxxxx 部分，方便后面正则过滤
img_src = soup.select('.game_header_image_full')[0].attrs['src'].split('?')[0]

# 去除数字到header之前的部分
img_src = re.sub(r'/(\d+)/[^/]+(/header[^/]+)', r'/\1\2', img_src)
if(img_src):
  # 替换header，获取竖图地址
  # img_src = img_src.replace('header','library_600x900')
  img_src = re.sub(r'(/header)[^/.]*\.', r'/library_600x900.', img_src)
print(img_src)
dl_img(img_src)

developers = get_dev_str(developers_a_list)
publishers = ''
tags = get_tags_str(tags_list)


# # 开发商字符串
# for i in range(len(developers_a_list)):
# #  print(developers_a_list[i].get_text())
#   developers += developers_a_list[i].get_text()
#   if(i != len(developers_a_list) - 1):
#     developers += ','
# print(developers)

# # 标签字符串
# for i in range(len(tags_list)):
# #  print(tags_list[i].get_text())
#   tags += tags_list[i].get_text()
#   if(i != len(tags_list) - 1):
#     tags += ' '
# print(tags)

# 发行商字符串
for i in range(len(developers_a_list), len(publishers_a_list)):
  publishers += publishers_a_list[i].get_text()
  if(i != len(publishers_a_list) - 1):
    publishers += ','

# print(publishers)
str_null = ''
text1 = """{{Infobox Game
|中文名= 
|别名={
}
|平台={
[PC]
}"""

text2 = f"""
|游戏类型= {tags}
|游玩人数= 1
|发行日期= {date}
|售价= $
|开发= {developers}
|发行= {publishers}
|website= {link}
|链接={{
[Steam|{url}]
"""

# lastLine = f"""

# """

# main_text = """
# {{Infobox Game
# |中文名= 
# |别名={
# }
# |平台={
# [PC]
# }
# |游戏类型= 解谜
# |游玩人数= 1
# |发行日期= 2023-03-01
# |售价= $7.99
# |开发= Rupour
# |发行= Rupour
# |website= https://www.blockappend.net/
# |链接= {
# [Steam|https://store.steampowered.com/app/xxxxxxx/]
# }
# }}
# """

# print(text1 + text2)

# 保存字符串为文本文件
def save_txt(file_name, file_content):
  with open(file_name.replace('/', '_') + ".txt", "w", encoding='utf-8') as f:
    f.write(file_content)

# main_text = text1 + text2 + '}}\n' + description
# main_text = text1 + text2 + '}\n}}\n' + description
main_text = text1 + text2 + '}\n}}'
# save_txt('test', text1 + text2 + description)
save_txt('test', main_text)


