import asyncio

async def request(url):
  print('now request ', url)
  print('request success')
  return url

# async修饰的函数，调用之后返回一个协程对象
c = request('www.baidu.com')



# # 创建一个事件循环对象
# loop = asyncio.get_event_loop()

# # 将协程对象注册到loop中，然后启动loop
# loop.run_until_complete(c)



# task的使用
# loop = asyncio.get_event_loop()
# # 基于loop创建了一个task对象
# task = loop.create_task(c)
# print(task)
# loop.run_until_complete(task)
# print(task)



# future的使用
# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(c)
# print(task)
# loop.run_until_complete(task)
# print(task)



def callback_func(task):
  # result返回的就是任务对象中封装的协程对象对应函数的返回值
  print(task.result())

# 绑定回调
# loop = asyncio.get_event_loop()
loop =  asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = asyncio.ensure_future(c)
# 将回调函数绑定到任务对象中
task.add_done_callback(callback_func)
loop.run_until_complete(task)

