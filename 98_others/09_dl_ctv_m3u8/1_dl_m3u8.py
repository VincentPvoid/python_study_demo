import requests
import re
import aiohttp
import aiofiles
import asyncio
import os


# 获取m3u8入口文件地址
def get_index_url(url):
  res = requests.get(url=url, verify=False)
  res.encoding = "utf-8"
  # print(res.text)
  regObj = re.compile(r"/asp/hls/850/.*m3u8", re.S)
  temp = regObj.search(res.text).group()
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
          line = line.strip()  # 1.ts等名称的ts文件
          # 拼接获取ts文件url 注意完整地址为https://hls.cntv.myhwcdn.cn/asp/hls/850/0303000a/3/default/92349d921f434c2d83c2d28d1cc2d024/xxx.ts
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
  output_file_name = 'TJGFR.mp4'
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


def main():
  # m3u8列表文件名称
  list_file_name = 'm3u8_list.txt'
  # 文件地址前缀
  base_url = "https://hls.cntv.myhwcdn.cn"

  # 视频对应入口地址
  page_url = "https://newcntv.qcloudcdn.com/asp/hls/main/0303000a/3/default/92349d921f434c2d83c2d28d1cc2d024/main.m3u8"
  m3u8_file_url = get_index_url(page_url)

  # ts文件名列表url
  m3u8_file_url = base_url + m3u8_file_url
  print(m3u8_file_url)
  # 请求该地址，下载列表m3u8文件
  dl_m3u8_file(m3u8_file_url, list_file_name)
  # 获取ts文件地址前缀 https://newcntv.qcloudcdn.com/asp/hls/main/0303000a/3/default/92349d921f434c2d83c2d28d1cc2d024/
  base_url = m3u8_file_url.replace('850.m3u8', '')
  # print(base_url)
  # 异步协程下载ts文件
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  asyncio.run(aio_dl_files(base_url, list_file_name))
  merge_ts(list_file_name)


if __name__ == '__main__':
  main()
