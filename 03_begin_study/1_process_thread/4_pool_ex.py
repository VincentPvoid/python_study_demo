# 线程池简单案例
# 1. 提取单个页面的数据
# 2. 使用线程池，多个页面同时抓取

import requests
import csv
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

fp = open('books_data.csv', mode='w', encoding='utf-8', newline='')
csvwriter = csv.writer(fp)

url = 'https://www.dushu.com/book/1107_1.html'


# 下载对应页面资料
def down_load_page(url):
  response = requests.get(url)
  tree = etree.HTML(response.text)
  # 获取数据列表容器
  div_list = tree.xpath("//div[@class='bookslist']/ul/li")
  for i in range(len(div_list)):
    # print(div_list[i], i)
    # 标题
    title = div_list[i].xpath('.//h3//a/@title')[0]
    # 作者
    author = div_list[i].xpath('.//p[1]/text()')[0]
    # 描述
    dec = div_list[i].xpath('.//p[2]/text()')[0]
    # print(title, author, dec)
    txt = [str(title) , str(author) ,str(dec)]
    # 把数据存放在文件中；注意参数是数组类型
    csvwriter.writerow(txt)
    # print(txt)
  print(url, 'finish')


def handle_text(text):
  content = text.strip()
  if (content.find(',') != -1):
    content = f'"{content}"'
  return content


if __name__ == '__main__':
  # down_load_page(url=url)
  # fp.close()
  # for i in range(1,100):  # 效率低下
  #   down_load_page(f'https://www.dushu.com/book/1107_{i}.html')
  # 创建线程池
  with ThreadPoolExecutor(50) as t:
    for i in range(1,100):
      # 把下载任务提交给线程池
      t.submit(down_load_page, url=f'https://www.dushu.com/book/1107_{i}.html' )
  fp.close()
  print('end')