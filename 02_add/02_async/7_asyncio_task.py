# import asyncio

# async def func():
#   print(1)
#   await asyncio.sleep(2)
#   print(2)
#   return 'something'

# async def main():
#   print('main start')
  
#   task_list = [
#     asyncio.create_task( func(), name='n1' ),
#     asyncio.create_task( func(), name='n2' )
#   ]

#   print('main end')
  
#   # 可以加入时间限制timeout；默认为None
#   done, pending = await asyncio.wait(task_list, timeout=None)
#   print(done)
#   # print(pending,'==========')

# asyncio.run(main())


import asyncio

async def func():
  print(1)
  await asyncio.sleep(2)
  print(2)
  return 'something'

task_list = [
  func(),
  func()
]
done, pending = asyncio.run(asyncio.wait(task_list))
print(done)