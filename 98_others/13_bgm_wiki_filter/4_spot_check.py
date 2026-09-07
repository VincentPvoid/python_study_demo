import concurrent.futures
import time
import requests
import random



def get_info_arr(content):
  # 获取返回信息数组
  info_arr = content['infobox']
  return info_arr


# 判断是否为需要的条目项（发行日期信息中是否包含 年 字段）
def is_tar_item(info_arr):
  date_val = get_date_val(info_arr)
  # 根据获取到的类型进行不同处理
  if isinstance(date_val, str):
    if (date_val.find('年') != -1):
      # list.append(url)
      return True
    return False
  elif isinstance(date_val, list):
    # 为list时需要获取列表项v字段的值（列表项结构 {k: xxx, v: date }）
    for i in range(len(date_val)):
      if (date_val[i]['v'].find('年') != -1):
        return True
  return False


# 获取发行日期信息；该值可能是list或者是str
def get_date_val(info_arr):
  for i in range(len(info_arr)):
    item_key = info_arr[i]['key']
    item_val = info_arr[i]['value']
    if (item_key == '发行日期'):
      return item_val
  return ''


# 从文件中读取url列表，并把url替换为api接口url
def read_url_list():
  list = []
  with open('./new_list.txt', mode='r', encoding='utf-8') as fp:
    for line in fp:
      url = line.strip().replace("https://bgm.tv/subject/",
                                 "https://api.bgm.tv/v0/subjects/")
      list.append(url)
  print(f"new list num: {len(list)}")
  return list


# 从列表中随机抽取条目；pick_num需要抽取的条目数
def sortition_url_list(ori_list, pick_num):
  list = []
  index_num = -1
  
  # 可以抽取的最大下标
  max_num = len(ori_list)

  if max_num <= pick_num:
    return ori_list
  
  for i in range(pick_num):
    # 从0到max_num（不包括max_num）之间的随机数
    index_num = random.randrange(0, max_num)
    list.append(ori_list[index_num])
    print(index_num)
  return list



# 处理请求列表，失败url需要重新请求；重试次数retry_left为3
def handle_list(url_list, tar_list, retry_left = 3):
  
  print(f"retry times: {3 - retry_left}")

  if (len(url_list) == 0 or retry_left <= 0):
    return
  
  info_arr = []
  error_list = []

  res_list = fetch_all_urls(url_list)
  
  for item in res_list:
    if item['success']:
      info_arr = get_info_arr(item['res'].json())
      if (is_tar_item(info_arr)):
        tar_list.append(item['url'])
    # 请求出错的结果
    else:
      error_list.append(item['url'])
  
  handle_list(error_list, tar_list, retry_left - 1)
  

# 请求并处理响应
def fetch_url(url):
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
  }
  try:
    # 设置超时为15秒
    response = requests.get(url, headers=headers, timeout=15)  
    # 如果请求失败，抛出HTTPError异常
    response.raise_for_status()  
    # 返回响应内容
    # return response
    
    # 因为后面还需要用到url，所以把url和结果都存入到一个对象中，再返回
    obj = {
      "url": url,
      "res": response,
      "success": True
    }
    return obj
  except requests.RequestException as e:
    print(f"Error fetching {url}: {e}")
    # return None
    # 出错时返回对象
    return {
      "url": url,
      "res": None,
      "success": False,
      "error": str(e)
    }




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
     
    results = executor.map(fetch_url, url_generator(url_list, 1))  
  # print(results)
  return results



# 把列表保存为文件
def save_list_to_txt(list, file_name="tar_list"):
  if not list:
    return
  
  # 追加模式
  with open(f'./{file_name}.txt', mode='a', encoding='utf-8') as fp:
    text = ''
    for i in range(len(list)):
      text += '\n' + list[i].replace("https://api.bgm.tv/v0/subjects/",
                              "https://bgm.tv/subject/")
    print(len(list))
    fp.write(text)





def main():
  
  url_list = read_url_list()
  # print(url_list)
  
  # 从原始列表中随机抽取30条数据进行检查
  random_list = sortition_url_list(url_list, 30)
  print(random_list)
  
  tar_list = []
  
  handle_list(random_list, tar_list, 3)
  
  print(tar_list)
  
  save_list_to_txt(tar_list)
  

if __name__ == '__main__':
  main()
