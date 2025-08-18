import requests
from bs4 import BeautifulSoup
import time
import concurrent.futures


# 自定义生成器，添加请求间隔（单位为秒）
def url_generator(url_list, interval):
  for url in url_list:
    yield url
    print(url)
    # 设置请求间隔
    time.sleep(interval)
    
    

# 请求并处理响应
def fetch_url(url):
  try:
    # 设置超时为15秒
    response = requests.get(url, timeout=15)
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
  
  

# 使用ThreadPoolExecutor并发发送请求
def fetch_all_urls(url_list, interval=1):
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # 使用executor.map来自动处理迭代和Future的获取
    # results = executor.map(fetch_url, url_list)

    results = executor.map(fetch_url, url_generator(url_list, interval))
  # print(results)
  return results



# 从文件中读取url列表
def read_link_list():
  link_list = []
  with open('./book_list.txt', 'r', encoding='utf-8') as fp:
    for line in fp:
      line = line.replace('\n', '')
      if len(line) != 0:
        link_list.append(line)
  return link_list



# 获取对应url中，物品库存不为0的项目列表
def get_inventory(list):
  tar_list = []
  for item in list:
    if item:
      content = item['res'].text
      soup = BeautifulSoup(content, 'lxml')
      # document.querySelector('.product_amounts option')
      tar_ele = soup.select('.product_amounts option')
      if (tar_ele):
        if (tar_ele[0]['value']):
          tar_list.append(item['url'])
  return tar_list


# 库存不为0的项目列表保存到文件中
def handle_inventory_list(list, file_name="inventory_list"):
  list_len = len(list)
  if list_len:
    with open(f'./{file_name}.txt', mode='w', encoding='utf-8') as fp:
      text = ''
      for i in range(list_len):
        text += list[i] + '\n'
      print(i + 1)
      fp.write(text)
  else:
    print("no available inventory")



def main():

  # test_list = ['https://www.suruga-ya.jp/product/detail/xxxxxxxx',
  #              'https://www.suruga-ya.jp/product/detail/xxxxxxxx']

  # res_list = fetch_all_urls(test_list)

  # for item in res_list:
  #   print(item['res'])
  #   print("============")
  #   print(item['res'].text)

  link_list = read_link_list()
  # print(link_list)
  # print(len(link_list))

  res_list = fetch_all_urls(link_list)
  tar_list = get_inventory(res_list)
  print(tar_list)

  handle_inventory_list(tar_list)


if __name__ == '__main__':
  main()
