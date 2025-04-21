import requests
from bs4 import BeautifulSoup
import re


# list = document.querySelectorAll('.line_list>li')
# list[index].innerText.include('新条目')
# list[index].querySelector('a').attributes['href']
# parseInt(document.querySelector('.p_edge').innerText.split('/')[1])


# 获取总页数
def get_total_page(soup):
  # print(soup.select('.p_edge')[0])
  temp = soup.select('.p_edge')[0].get_text()
  temp = temp.split('/')[1]
  page = re.findall(r'\d+', temp)
  # print(temp)
  return page[0]


# 判断当前是否为新条目
def is_new_item(ele_item):
  index = ele_item.get_text().find('新条目')
  if (index != -1):
    return True
  else:
    return False


# 获取条目项的跳转地址
def get_link(ele_item):
  a = ele_item.find('a')
  # print(a)
  base_url = 'https://bgm.tv'
  return base_url + a.attrs['href']


# 保存字符串为文本文件
def save_txt(file_name, file_content):
  with open(file_name.replace('/', '_') + ".txt", "w", encoding='utf-8') as f:
    f.write(file_content)


# 把获取到的新条目列表保存为文件
def save_url_to_txt(list, file_name="new_list"):
  with open(f'./{file_name}.txt', mode='w', encoding='utf-8') as fp:
    text = ''
    for i in range(len(list)):
      text += list[i] + '\n'
    # text += f'\n共{i+1}条'
    print(i+1)
    fp.write(text)


# 获取对应页面的新条目项
def get_new_list(user_id, page_num=1, new_list=[]):
  url = f"""https://bgm.tv/user/{user_id}/wiki?page={page_num}"""

  print(url)

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
  }

  proxy = {'https': 'http://127.0.0.1:7890', 'http': 'http://127.0.0.1:7890'}

  response = requests.get(url=url, proxies=proxy, headers=headers)
  response.encoding = "utf-8"
  content = response.text
  soup = BeautifulSoup(content, 'lxml')

  li_list = soup.select('.line_list>li')

  # print(get_link(li_list[0]))
  # print(is_new_item(li_list[3]))

  for i in range(len(li_list)):
    # 如果当前为新增条目，则放入列表中
    if (is_new_item(ele_item=li_list[i])):
      link = get_link(li_list[i])
      new_list.append(link)



def init(user_id='target_user_id'):
  url = f"""https://bgm.tv/user/{user_id}/wiki?page=1"""
  # url = base_url + '?page=' + page_num

  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
  }

  proxy = {'https': 'http://127.0.0.1:7890', 'http': 'http://127.0.0.1:7890'}

  response = requests.get(url=url, proxies=proxy, headers=headers)
  response.encoding = "utf-8"
  content = response.text
  soup = BeautifulSoup(content, 'lxml')
  # print(content)
  # save_txt('test', content)
  
  # 获取总页数
  total_page = int(get_total_page(soup))
  print(total_page)

  # 新增条目项url列表
  new_list = []

  for i in range(total_page):
    get_new_list(user_id=user_id, page_num=i+1, new_list=new_list)

  # print(new_list)
  save_url_to_txt(new_list)


def main():
  # get_new_list()
  init()
  # pass


if __name__ == '__main__':
  main()
