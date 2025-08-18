import requests
from bs4 import BeautifulSoup

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
  for i in range(len(list)):
    url = list[i]
    response = requests.get(url=url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    # document.querySelector('.product_amounts option')
    tar_ele = soup.select('.product_amounts option')
    if (tar_ele):
      if(tar_ele[0]['value']):
        tar_list.append(list[i])
  return tar_list

# 库存不为0的项目列表保存到文件中
def handle_inventory_list(list, file_name="inventory_list"):
  list_len = len(list)
  if list_len:
    with open(f'./{file_name}.txt', mode='w', encoding='utf-8') as fp:
      text = ''
      for i in range(list_len):
        text += list[i] + '\n'
      print(i)
      fp.write(text)
  else:
    print("no available inventory")



def main():
  
  # url = 'https://www.suruga-ya.jp/product/detail/xxxxxxxxx' # 有
  # # url = 'https://www.suruga-ya.jp/product/detail/xxxxxxxxx' # 无
  # response = requests.get(url=url)
  # content = response.text
  # print(content)
  # soup = BeautifulSoup(content, 'lxml')
  # # document.querySelector('.product_amounts option')
  # tar_ele = soup.select('.product_amounts option')
  # if(tar_ele):
  #   print((tar_ele[0]['value']))
  #   # print(type(int(tar_ele[0]['value'])))
  # else:
  #   print("sell out")
  
  link_list = read_link_list()
  print(link_list)
  print(len(link_list))
  
  tar_list = get_inventory(link_list)
  print(tar_list)
  
  handle_inventory_list(tar_list)
  
  
  
  


if __name__ == '__main__':
  main()
