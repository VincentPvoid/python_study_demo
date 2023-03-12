import re
import json

# 需要的字符串字段
# content="xxxxxx" 内容
# publishTime=xxxxxx 发表时间
# tag="xxx,xx" 标签，如果有多个，其中用,分割

# 获取内容正则
contentReg = re.compile('\.content="(.*?)";')
# 获取时间正则
timeReg = re.compile('\.publishTime=([0-9]+);')
# 获取标签正则
tagsReg = re.compile('\.tag=(.*?);')

# with open('./ori_text/daily_ori_page0.txt', 'r', encoding='utf-8') as fp:
#   content = fp.read()
#   content_list = re.findall(contentReg, content)
#   time_list = re.findall(timeReg, content)
#   tags_list = re.findall(tagsReg, content)


# daily_data_list = []

# for i in range(len(content_list)):
#   if(content_list[i] == 'content'):
#     print(i)
#     continue

#   content = content_list[i].encode('latin-1').decode('unicode_escape')
#   publish_time = time_list[i]
#   tags = tags_list[i].encode('latin-1').decode('unicode_escape')
#   data = {
#     "content": content,
#     "publish_time": publish_time,
#     "tags": tags,
#   }
#   daily_data_list.append(data)
#   # print(data)

# with open('./daily_json/dairy_json0.json', 'w', encoding='utf-8') as fp:
#   # fp.write(str(daily_data_list))
#   # Python3已经将 Unicode 作为默认编码
#   # Python3中的 json 库在做 dumps 操作时，会将中文转换成 Unicode 编码，并以 16 进制方式存储。
#   # 再做逆向操作时，会将 Unicode 编码转换回中文。
#   # 所以加上ensure_ascii=False，直接保存中文
#   json.dump(daily_data_list, fp, ensure_ascii=False)

# print(type(daily_data_list))

# 获取所有文本
def get_text_data(num):
  with open(f'./ori_text/daily_ori_page{num}.txt', 'r', encoding='utf-8') as fp:
    content = fp.read()
  return content

# 获取对应数据，并放入一个数组中
def get_json_list(content):
  content_list = re.findall(contentReg, content)
  time_list = re.findall(timeReg, content)
  tags_list = re.findall(tagsReg, content)
  daily_data_list = []
  for i in range(len(content_list)):
    if(content_list[i] == 'content'):
      print(i)
      continue

    # 把unicode转码为中文
    content = content_list[i].encode('latin-1').decode('unicode_escape')
    tags = tags_list[i].encode('latin-1').decode('unicode_escape')
    publish_time = time_list[i]

    data = {
      "content": content,
      "publish_time": publish_time,
      "tags": tags,
    }
    daily_data_list.append(data)
  return daily_data_list

# 把数组保存为json文件
def save_json(num,daily_data_list):
  with open(f'./daily_json/dairy_json{num}.json', 'w', encoding='utf-8') as fp:
  # fp.write(str(daily_data_list))
  # Python3已经将 Unicode 作为默认编码
  # Python3中的 json 库在做 dumps 操作时，会将中文转换成 Unicode 编码，并以 16 进制方式存储。
  # 再做逆向操作时，会将 Unicode 编码转换回中文。
  # 所以加上ensure_ascii=False，直接保存中文
    json.dump(daily_data_list, fp, ensure_ascii=False)



if __name__ == '__main__':
  for i in range(4):
    # print(i)
    content = get_text_data(i)
    list = get_json_list(content)
    save_json(i, list)


