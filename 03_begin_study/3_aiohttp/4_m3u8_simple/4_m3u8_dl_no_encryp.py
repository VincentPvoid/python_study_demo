# 步骤
# 1. 查看主页面的页面源代码，找到iframe
# 2. 在iframe的页面源代码中找到m3u8文件
# 3. 下载第一层m3u8文件 -> 下载第二层m3u8文件
# 4. 下载视频片段
# 5. 下载秘钥，进行解密
# 6. 合并所有ts文件为一个视频文件

import requests
import re
import aiohttp
import aiofiles
import asyncio
import os


# 获取m3u8入口文件url地址
def get_index_url(url):
  res = requests.get(url=url, verify=False)
  res.encoding = "utf-8"
  # print(res.text)
  # 处理返回的html字符串，获取第一层m3u8文件地址

  # 使用分割字符串的方法提取网址
  # temp = res.text.split('"url":"h')[1].split('","url_next"')[0]
  # temp = 'h' + temp.replace('\\', '')

  # 使用正则提取网址
  # r代表原字符串，这种写法可以直接写特殊符号，不用加\等转义符
  regObj = re.compile(r'"url":"h(?P<m3u8_url>.*?)",', re.S)
  temp = regObj.search(res.text).group('m3u8_url')
  # 提取到的字符串中带有转义符\，需要去除
  temp = 'h' + temp.replace('\\', '')
  print(temp)
  return temp


# 下载m3u8文件
def dl_m3u8_file(url, file_name):
  res = requests.get(url)
  with open(file_name, mode="wb") as fp:
    fp.write(res.content)


# 创建异步队列
async def aio_dl_files(base_url, file_name):
  tasks = []
  # 创建会话并作为参数传递到下载队列中，这样就不需要下载一个文件就打开一个会话
  async with aiohttp.ClientSession() as session:
    async with aiofiles.open(file_name, mode="r", encoding='utf-8') as fp:
      async for line in fp:
        if line.startswith('#'):
          continue
        else:
          # 去除该行中的空格和换行符
          line = line.strip()  # b5ee82c52d7000000.ts等名称的ts文件
          # 拼接获取ts文件url 注意完整地址为https://vip.lz-cdn1.com/20220606/7685_fba34b24/1200k/hls/xxxxx.ts这种格式
          ts_url = base_url + line
          print(ts_url)
          # 创建下载任务
          c = asyncio.create_task(dl_ts(ts_url, line, session))
          # 把下载任务加入队列
          tasks.append(c)
      # 等待下载任务结束
      await asyncio.wait(tasks)


# 下载ts视频片段文件并保存
async def dl_ts(url, file_name, session):
  # headers = {
  #   "origin": "https://www.hnjiexi.com",
  #   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
  # }
  # 限制最大线程为50个
  sem = asyncio.Semaphore(50)
  async with sem:
    async with session.get(url=url) as res:
      # print(res.content.read())
      async with aiofiles.open(f'video_ts/{file_name}', mode="wb") as fp:
        # fp.write(await BytesIO(res.content))
        # read()读取结果也是异步过程，因此需要await
        await fp.write(await res.content.read())
    print(file_name, 'finish')

# 按顺序合并所有ts文件
def merge_ts(list_file_name):
  # mac： cat 1.ts 2.ts 3.ts > xxx.mp4
  # win： copy /b 1.ts+2.ts+3ts xxx.mp4
  # 拼接的字符串太长了无法用这种方法合并
  # list = []
  # with open(list_file_name, mode='r', encoding='utf-8') as fp:
  #   for line in fp:
  #     if line.startswith('#'):
  #       continue
  #     line = line.strip()
  #     # 在win下使用/可能会有问题，所以使用\
  #     list.append('.\\video_ts\\' + line)
  # namesStr = "+".join(list)
  # os.system(f"copy /b {namesStr} TMWFTWS1E01.mp4")

  # 使用ffmpeg合并
  # ts文件名列表文件名称
  merge_list_file_name = 'merge_ts_names_list.txt'
  path = './video_ts'
  list = []
  with open(list_file_name, mode='r', encoding='utf-8') as fp:
    for line in fp:
      if line.startswith('#'):
        continue
      line = line.strip()
      list.append(line)
  # print(list)
  with open(merge_list_file_name, mode="w", encoding='utf-8') as fp:
    for item in list:
      fp.write(f"file {path}/{item}\n")
  output_file_name = 'TMWFTW.mp4'
  # 合并命令字符串格式；xxx.txt文件名列表文件，格式 file xxx.ts换行file xxx.ts；yyy.mp4合并后输出文件名
  # ffmpeg -f concat -i xxx.txt -c copy yyy.mp4
  # 直接使用该命令会报Unsafe file name错误，可添加-safe 0参数解决
  # safe值默认为1，拒绝使用不安全的文件路径；安全的文件路径的.不能放在开头
  # safe值设置为0，则接受所有的文件名
  cmd_str = f"ffmpeg -f concat -safe 0 -i {merge_list_file_name} -c copy {output_file_name}"
  print(cmd_str)
  try:
    # 执行合并命令
    os.system(cmd_str)
  except Exception as e:
      print(e)
  print("merge finish")



if __name__ == '__main__':
  # m3u8入口文件名称
  index_file_name = 'm3u8_index_TMWFTW.txt'
  # m3u8列表文件名称
  list_file_name = 'm3u8_list_TMWFTW.txt'

  # 1. 查看主页面的页面源代码，找到iframe
  # 实际使用这个案例在源代码中没有iframe，需要处理返回的html代码获取第一层的入口m3u8文件地址
  page_url = 'https://www.999mjtv.com/vodplay/8244-2-1.html'
  # 2. 在iframe的页面源代码中找到m3u8文件
  index_m3u8_url = get_index_url(page_url)  # https://vip.lz-cdn1.com/20220606/7685_fba34b24/index.m3u8
  # index_m3u8_url = 'https://vip.lz-cdn1.com/20220606/7685_fba34b24/index.m3u8'
  base_url = ''
  # 3. 下载第一层m3u8文件 -> 下载第二层m3u8文件
  dl_m3u8_file(index_m3u8_url, index_file_name)
  with open(index_file_name, mode="r", encoding='utf-8') as fp:
    # 读取该文件每一行
    for line in fp:
      # 如果以#开头则忽略该行
      if line.startswith('#'):
        continue
      else:
        # 去除该行中的空格和换行符
        line = line.strip()  # 1200k/hls/index.m3u8
        # 拼接获取第二层m3u8列表文件的url地址
        # https://vip.lz-cdn1.com/20220606/7685_fba34b24/
        list_m3u8_url = index_m3u8_url.split('index.m3u8')[0] + line  # https://vip.lz-cdn1.com/20220606/7685_fba34b24/1200k/hls/index.m3u8
        base_url = list_m3u8_url.replace('index.m3u8', '')
        # 下载列表m3u8文件
        dl_m3u8_file(list_m3u8_url, list_file_name)
  # 获取ts文件地址前缀 https://vip.lz-cdn1.com/20220606/7685_fba34b24/1200k/hls/
  base_url = index_m3u8_url.split('index.m3u8')[0]
  # 异步协程
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(aio_dl_files(base_url, list_file_name))
  merge_ts(list_file_name)
