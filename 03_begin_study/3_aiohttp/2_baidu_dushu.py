# 爬取全本小说

# 获取所有小说章节cid
# http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306063500"}
# book_id小说id；cid章节id；need_bookinfo值为1
# http://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782339", "need_bookinfo":1}

import asyncio
import aiohttp
import aiofiles
import requests
import json


"""""
1. 同步操作：访问getCatalog，获取所有章节cid和名称
2. 异步操作：访问getChapterContent，下载所有文章内容
""" ""

# 获取所有章节名称和cid
async def getCatalog(book_id):
  # 注意url的格式，一定要是这种形式才能请求到数据
  url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"' + book_id + '"}'
  # print(url)
  response = requests.get(url=url)
  # print(response.json())
  res_obj = response.json()
  tasks = []
  for item in res_obj['data']['novel']['items']:
    title = item['title']
    cid = item['cid']
    # print(title, cid)
    # 封装task对象，准备异步任务
    c = asyncio.create_task(download_chapters(book_id,cid, title))
    tasks.append(c)
  await asyncio.wait(tasks)

# 获取所有章节并保存为文件
async def download_chapters(book_id, cid, title):
  data = {
    "book_id":book_id,
    "cid": f"{book_id}|{cid}",
    "need_bookinfo": 1,
  }
  # 注意需要先转换为json字符串，否则可能会因为不是"双引号的问题而无法请求成功
  data = json.dumps(data)
  url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={data}"
  # print(url)
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
      # 注意此处等待响应返回并转换为json格式也是异步操作，需要加await
      res_obj = await resp.json()
      content = res_obj['data']['novel']['content']
      # 使用异步文件操作模块aiofiles
      async with aiofiles.open(title+'.txt', mode='w', encoding='utf-8') as fp:
        # 把文章内容写入文件
        await fp.write(content)

      




if __name__ == '__main__':
  # getCatalog('4306063500')
  book_id = '4306063500'
  asyncio.run(getCatalog(book_id))
