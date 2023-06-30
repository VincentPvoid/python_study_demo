# 下载字幕zip文件

import requests
from bs4 import BeautifulSoup
import aiohttp
import aiofiles
import asyncio

# 下载字幕前缀
# base_url = "https://dl.opensubtitles.org/en/download/sub/"
# 入口页面地址
# index_url = "https://www.opensubtitles.org/en/ssearch/sublanguageid-all/idmovie-xxxxxxx"

# 获取url所需的列表；包含需要的url字段、字幕文件名
def get_target_list(url):
  list = []
  res = requests.get(url=url)
  content = res.text
  # print(content)
  soup = BeautifulSoup(content, 'lxml')
  # # //form[@id='submultiedit']//td[starts-with(@id,'main')]/@id
  # //form[@id='submultiedit']//td[starts-with(@id,'main')]/span/@title
  td_ele_list = soup.select('#submultiedit td[id^="main"]')
  for i in range(len(td_ele_list)):
    # 下载需要的url字段
    str = td_ele_list[i].attrs['id'].split('main')[1]
    # 对应文件名称
    temp = td_ele_list[i].find('span')

    # 有可能为空，所以需要进行处理；没有文件名的不存入列表中
    if(temp):
      temp = temp.attrs['title']
      obj = {
        "url" : str,
        "name" : temp
      }
      list.append(obj)

    # print(temp)
  # print(list,len(list))
  return list

# 创建异步下载（字幕）文件队列
async def aio_dl_task(base_url, list):
  tasks = []
  async with aiohttp.ClientSession() as session:
    for item in list:
      url = base_url + item['url']
      print(url)
      c = asyncio.create_task(dl_subs(url, item['name'], session))
      tasks.append(c)
    await asyncio.wait(tasks)

# 下载字幕zip文件并保存
async def dl_subs(url, file_name, session):
  headers = {
    "Referer": "https://www.opensubtitles.org/en/search/sublanguageid-all/pimdbid-xxxxxx",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Cookie": "your cookie"
  }
  async with session.get(url=url, headers=headers) as res:
    async with aiofiles.open(f'sub_zip/{file_name}.zip', mode="wb") as f:
      await f.write(await res.content.read())
  print(file_name, 'download finish')



def main():
  page_url = "https://www.opensubtitles.org/en/search/sublanguageid-all/pimdbid-xxxxxxx"
  base_url = "https://dl.opensubtitles.org/en/download/sub/"
  
  list = get_target_list(page_url)
  
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(aio_dl_task(base_url, list))


  # list = get_target_list(page_url)
  # for item in list:
  #   print(item)
  # 请求测试
  # headers = {
  #   "Referer": "https://www.opensubtitles.org/en/search/sublanguageid-all/pimdbid-xxxxxx",
  #   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
  #   "Cookie": "your cookie"
  # }
  # res = requests.get(url='https://dl.opensubtitles.org/en/download/sub/xxxxxx',headers=headers)
  # # 这里返回的前缀为b'PK格式，表示为zip文件
  # content = res.content
  # print(content.decode)

if __name__ == '__main__':
  main()