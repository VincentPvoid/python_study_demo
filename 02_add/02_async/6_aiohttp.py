
# 需要安装aiohttp模块
import asyncio
import time
import aiohttp

start = time.time()

urls = [
  'http://127.0.0.1:3000/aaa',
  'http://127.0.0.1:3000/bbb',
  'http://127.0.0.1:3000/ccc',
]

tasks = []

async def get_page(url):
  async with aiohttp.ClientSession() as session:
    async with await session.get(url) as response:
      # 注意：获取响应数据之前一定要使用await进行手动挂起
      page_text = await response.text()
      print(page_text)


for url in urls:
  c = get_page(url)
  task = asyncio.ensure_future(c)
  tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('duration: ', end-start)
