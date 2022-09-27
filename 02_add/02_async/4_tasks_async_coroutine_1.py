import asyncio
import time

async def request(url):
  print('downloading...', url)
  # 在异步任务中如果使用了同步相关的代码，则无法实现异步
  # 如果使用了以下代码则无法异步
  # time.sleep(2)

  # 在asyncio中遇到阻塞操作必须进行手动挂起
  # 需要等待2s需要使用下面的代码才能实现异步
  await asyncio.sleep(2)

  print('finished', url)

start = time.time()
urls = [
  'www.baidu.com',
  'www.douban.com',
  'www.zhihu.com',
]

# 任务列表；存放多个任务对象
tasks = []

for url in urls:
  c = request(url)
  task = asyncio.ensure_future(c)
  tasks.append(task)
  # asyncio.run(task)

# 生成或获取一个事件循环
loop = asyncio.get_event_loop()
# 将任务列表封装到wait中（将任务放入任务列表）
loop.run_until_complete(asyncio.wait(tasks))


print(time.time() - start)


