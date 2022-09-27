# 多任务异步协程

import asyncio
import time


# 例1
# async def fun():
#   print('hello world')

# if __name__ == '__main__':
#   res = fun() # 此时的函数是异步协程函数，执行得到的是一个协程对象
#   # print(res) # 没有使用异步函数，直接使用会报错
#   asyncio.run(res) # 协程程序运行需要asyncio模块的支持

# 例2
# async def fn1():
#   print('111')
#   # time.sleep(2) # 在异步任务中如果使用了同步相关的代码，则无法实现异步
#   # 需要使用异步操作
#   await asyncio.sleep(2)
#   print('111')


# async def fn2():
#   print('222')
#   # time.sleep(3)
#   await asyncio.sleep(3)
#   print('222')


# async def fn3():
#   print('333')
#   # time.sleep(4)
#   await asyncio.sleep(4)
#   print('333')


# if __name__ == '__main__':
#   tasks = [fn1(), fn2(), fn3()]
#   start_time = time.time()

#   # 一次性启动多个任务（协程）
#   asyncio.run(asyncio.wait(tasks))

#   end_time = time.time()
#   print(end_time - start_time)



async def fn1():
  print('111')
  # 需要使用异步操作
  await asyncio.sleep(2)
  print('111')


async def fn2():
  print('222')
  await asyncio.sleep(3)
  print('222')


async def fn3():
  print('333')
  await asyncio.sleep(4)
  print('333')


async def main():
  # 第一种写法
  # f1 = fn1()
  # # 一般把await挂起操作放在协程对象前面
  # await f1 

  # 第二种写法（推荐）
  tasks = [ fn1(), fn2(), fn3() ]
  await asyncio.wait(tasks)


# if __name__ == '__main__':
#   start_time = time.time()
#   # 一次性启动多个任务（协程）
#   asyncio.run(main())
#   print(time.time() - start_time)



# 在爬虫领域的应用（模拟）
async def download(url):
  print('start...')
  await asyncio.sleep(2) # 网络请求
  print('finish')

async def main():
  urls = [
    'www.baidu.com',
    'www.douban.com',
    'www.zhihu.com',
  ]
  tasks = []
  # for url in urls:
  #   c = download(url)
  #   tasks.append(c)
  # await asyncio.wait(tasks)

  # 在python3.8后直接把协程对象传给asyncio.wait()会有警告，必须先封装成tasks对象再传入
  for url in urls:
    c = asyncio.create_task(download(url))
    tasks.append(c)
  await asyncio.wait(tasks)


if __name__ == '__main__':
  asyncio.run(main())