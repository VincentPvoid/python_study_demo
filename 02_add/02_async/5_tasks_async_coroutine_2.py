import requests
import asyncio
import time

start = time.time()

urls = [
  'http://127.0.0.1:3000/aaa',
  'http://127.0.0.1:3000/bbb',
  'http://127.0.0.1:3000/ccc',
]

tasks = []

async def get_page(url):
  print('downloading... ', url)
  # request.get是同步请求，因此需要使用基于异步的网络请求模块进行指定url的请求发送
  response = requests.get(url=url)
  print('finish ', url)


for url in urls:
  c = get_page(url)
  task = asyncio.ensure_future(c)
  tasks.append(task)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('duration: ', end-start)
