import requests
from bs4 import BeautifulSoup
from dateutil import parser
import re
import concurrent.futures
import time
import json




# 日期格式转换 转换为YYYY-MM-DD这种格式
def format_date(date_str):
  datetime_struct = parser.parse(date_str)
  return datetime_struct.strftime('%Y-%m-%d')

# 下载图片
def dl_img(url, img_name = 'header.jpg'):
  res = requests.get(url)
  with open(img_name, mode="wb") as fp:
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

# 判断对应对象中是否存在指定key和对应的value，如果都存在则存为字符串
def build_string_from_dict(obj, tar_list):
  text = ""
  for item in tar_list:
    for key, value in item.items():
      if key in obj and obj[key]:
        text += f"[{value}|{obj[key]}]\n"
  return text


# 处理steam商店页面响应，获取后半段字符串
def handle_main_url(res):
  content = res.text
  soup = BeautifulSoup(content, 'lxml')

  # 日期；如果未定获取到的字符串为To be announced 或 Coming soon
  date = soup.select('.date')[0].get_text()
  # print(date)
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
  try:
    link = soup.select('.details_block .linkbar')[0].attrs['href'].replace('%2F','/').replace('%3A', ':')
  except:
    link = ""
  # print(link)
  
  
  # # 获取图片地址，并去除后面的时间参数 ?=xxxxxx 部分，方便后面正则过滤
  img_src = soup.select('.game_header_image_full')[0].attrs['src'].split('?')[0]
  
  # 去除数字到header之前的部分
  img_src = re.sub(r'/(\d+)/[^/]+(/header[^/]+)', r'/\1\2', img_src)
  if(img_src):
    # 替换header，获取竖图地址
    img_src = re.sub(r'(/header)[^/.]*\.', r'/library_600x900.', img_src)
  print(img_src)
  dl_img(img_src)
  
  developers = get_dev_str(developers_a_list)
  publishers = ''
  tags = get_tags_str(tags_list)
  
  # 发行商字符串
  for i in range(len(developers_a_list), len(publishers_a_list)):
    publishers += publishers_a_list[i].get_text()
    if(i != len(publishers_a_list) - 1):
      publishers += ','
      
  text2 = f"""
|游戏类型= {tags}
|游戏引擎= 
|游玩人数= 1
|发行日期= {date}
|售价= $
|开发= {developers}
|发行= {publishers}
|website= {link}
|链接={{
[Steam|{url}]
"""
  return text2


# 处理steamcmd响应，获取前半段字符串和竖向大图
def handle_steamcmd_url(res):
  # res.encoding = 'utf-8'
  
  # 把字符串转换为json，方便获取对应值
  res_json = json.loads(res.text)
  # 竖图地址
  img_src = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{app_id}/" + res_json['data'][app_id]['common']['library_assets_full']['library_capsule']['image']['english']
  print(img_src)
  dl_img(img_src, 'header2.jpg')
  
  # 需要的语种标题列表
  tar_list = [{'tchinese':'繁中'}, {'japanese':'日文'}, {'koreana':'韩文'}]
  # 获取到的不同语种标题
  title_obj = res_json['data'][app_id]['common']['name_localized']
  # 获取当前有的标题字段
  title_text_part = build_string_from_dict(title_obj, tar_list)
  ch_title = title_obj.get('schinese', '')
  
  platforms = ["PC"]
  # 将列表转为换行分隔的字符串
  platforms_str = "\n".join(f"[{p}]" for p in platforms)
    
  text1 = f"""{{{{Infobox Game
|中文名= {ch_title}
|别名= {{
{title_text_part}
}}
|平台= {{
{platforms_str}
}}
"""
  return text1


# 请求并处理响应
def fetch_url(url):
  proxy = {'https': 'http://127.0.0.1:7890', 'http': 'http://127.0.0.1:7890'}
  try:
    response = requests.get(url=url, proxies=proxy)
    # 如果请求失败，抛出HTTPError异常
    response.raise_for_status()  
    # 返回响应内容
    # return response
    
    # 因为后面还需要用到url，所以把url和结果都存入到一个对象中，再返回
    obj = {
      "url": url,
      "res": response
    }
    return obj
  except requests.RequestException as e:
    print(f"Error fetching {url}: {e}")
    return None

# 自定义生成器，添加请求间隔
def url_generator(url_list, interval):
  for url in url_list:
    yield url
    print(url)
    # 设置请求间隔
    time.sleep(interval)
    
# 使用ThreadPoolExecutor并发发送请求  
def fetch_all_urls(url_list):  
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  
    # 使用executor.map来自动处理迭代和Future的获取  
    # results = executor.map(fetch_url, url_list) 
     
    results = executor.map(fetch_url, url_generator(url_list, 0))  
  # print(results)
  return results



# steam页面地址
url = input('target steam url: ')

# 替换获取steamcmd请求地址
steamcmd_url = re.sub('store.steampowered.com/app', 'api.steamcmd.net/v1/info', url)

# 获取steam应用id
app_id = url.rstrip("/").split("/")[-1] 

# url对应处理函数map
url_handler_map = {
  url: handle_main_url,
  steamcmd_url: handle_steamcmd_url
}

url_list = [steamcmd_url, url]
res_list = fetch_all_urls(url_list)

main_text = ''
for item in res_list:
  if item is not None:
    # print(item.get('url'), item.get('res').text)
    main_text += url_handler_map[item.get('url')](item.get('res'))

# 去除多余空行
main_text = re.sub(r'\n{2,}', '\n', main_text.strip())
# 添加结尾
main_text += '\n}\n}}'
# print(text1 + text2)

# 保存字符串为文本文件
def save_txt(file_name, file_content):
  with open(file_name.replace('/', '_') + ".txt", "w", encoding='utf-8') as f:
    f.write(file_content)


save_txt('test', main_text)


