from dateutil import parser
import requests


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


# ori_text 需要插入内容的文本；
# search_text 需要搜索的目标文本，用于确定插入位置；
# insert_text 需要插入的文本内容
def search_insert_text(ori_text, search_text, insert_text):
  lines = ori_text.splitlines(keepends=True)
  insert_positions = set()
  for i, line in enumerate(lines):
    if line.startswith(search_text):               # 该行开头是否为搜索值
      if i == 0:
        insert_positions.add(0)           # 第一行之前插入
      else:
        insert_positions.add(i)           # 在第 i 行之前插入（即原第 i-1 行之后）
  for pos in sorted(insert_positions, reverse=True):
    lines.insert(pos, insert_text + '\n')
  return ''.join(lines)