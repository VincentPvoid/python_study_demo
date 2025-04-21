import concurrent.futures
import time
import requests
import re


# 获取信息数组
# def get_info_arr(url):
#   headers = {
#       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
#   }

#   # 使用api接口（直接返回json，不需要去网页进行提取）
#   url = url.replace("https://bgm.tv/subject/",
#                     "https://api.bgm.tv/v0/subjects/")
#   print(url)

#   response = requests.get(url=url, headers=headers)
#   content = response.json()
#   # print(content)

#   # 获取返回信息数组
#   info_arr = content['infobox']
#   return info_arr



def get_info_arr(content):
  # 获取返回信息数组
  info_arr = content['infobox']
  return info_arr


# 判断是否为需要的条目项（发行日期信息中是否包含 年 字段）
def is_tar_item(info_arr):
  for i in range(len(info_arr)):
    item_key = info_arr[i]['key']
    item_val = info_arr[i]['value']
    if (item_key == '发行日期'):
      if (item_val.find('年') != -1):
        # list.append(url)
        return True
      return False
  return False


# 从文件中读取url列表，并把url替换为api接口url
def read_url_list():
  list = []
  with open('./test_list.txt', mode='r', encoding='utf-8') as fp:
    for line in fp:
      url = line.strip().replace("https://bgm.tv/subject/",
                                 "https://api.bgm.tv/v0/subjects/")
      list.append(url)
  return list


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
     
    results = executor.map(fetch_url, url_generator(url_list, 0.1))  
  # print(results)
  return results

  # 处理结果
  # for res in results:  
  #   if res is not None:  
  #     # print(f"Fetched content from a URL (truncated): {res}...")
  #     print(res['res'].json())
      

# 把列表保存为文件
def save_list_to_txt(list, file_name="tar_list"):
  with open(f'./{file_name}.txt', mode='w', encoding='utf-8') as fp:
    text = ''
    for i in range(len(list)):
      text += list[i].replace("https://api.bgm.tv/v0/subjects/",
                              "https://bgm.tv/subject/") + '\n'
    # text += f'\n共{i+1}条'
    print(i+1)
    fp.write(text)





def main():
  url_list = read_url_list()
  print(url_list)
  
  res_list = fetch_all_urls(url_list)

  tar_list = []
  info_arr = []
  
  for item in res_list:
    if item is not None:
      info_arr = get_info_arr(item['res'].json())
      if (is_tar_item(info_arr)):
        tar_list.append(item['url'])

  # for i in range(len(url_list)):
  #   url = url_list[i]
  #   info_arr = get_info_arr(url)
  #   # is_tar_item(info_arr, url, tar_list)
  #   if (is_tar_item(info_arr)):
  #     tar_list.append(url)

  print(tar_list)
  
  save_list_to_txt(tar_list)
  
  # url = "https://api.bgm.tv/v0/subjects/544350"
  # tar_list = []
  # info_arr = get_info_arr(url)
  # is_tar_item(info_arr, url, tar_list)

  # pass


if __name__ == '__main__':
  main()
