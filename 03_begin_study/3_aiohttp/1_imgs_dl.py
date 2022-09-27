# 异步请求
# 需要使用aiohttp模块

import aiohttp
import asyncio

# 图片地址url
urls = [
  'url1','url2','url3'
]

async def aiodownload(url):
  # 发送请求
  # 获取图片内容
  # 保存到文件
  # s = aiohttp.ClientSession()   等同于 requests的功能
  # s.get()  .post   等同于  requests.get() post()的功能
  # with...as 写法可自动关闭打开的文件/会话等对象，可以省去手动关闭的操作
  
  # rsplit表示从右开始进行分割，切一次，获取[1]位置的内容
  img_name = url.rsplit('/', 1)[1]
  async with aiohttp.ClientSession() as session:
    # 发送请求
    async with session.get(url) as resp:
      # 请求返回响应后，把图片文件写入文件
      # 文件操作可以使用aiofiles模块来提高效率
      with open(img_name, mode='wb') as fp:
        # 创建文件；文件读写操作是异步的，因此需要await挂起
        fp.write(await resp.content.read())
  print(img_name, 'finish')

  

async def main():
  tasks = []
  for url in urls:
    c = asyncio.create_task(aiodownload(url))
    tasks.append(c)
  await asyncio.wait(tasks)

# # important
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
  # 下面语句可以实现下载图片效果，但会报错
  # RuntimeError: Event loop is closed
  # asyncio.run(main())
  
  # 下面语句可以实现下载图片效果，但会有警告
  # DeprecationWarning: There is no current event loop
  # loop = asyncio.get_event_loop()
  # loop.run_until_complete(main())

  # 因为windows 系统对于 https 网站，会出现错误
  # 加入以下语句则不会报错
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(main())