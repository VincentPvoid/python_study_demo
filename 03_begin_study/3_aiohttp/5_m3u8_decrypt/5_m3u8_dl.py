# 流程
# index.m3u8地址： iframe中的data-play属性值
# 对该值进行2次base64解密，可获取入口m3u8地址


# 步骤
# 1. 查看主页面的页面源代码，找到iframe；
#   index.m3u8地址： iframe中的data-play属性值
#   对该值进行2次base64解密，可获取入口m3u8地址
# 2. 在iframe的页面源代码中找到m3u8文件
# 3. 下载第一层m3u8文件 -> 下载第二层m3u8文件
# 4. 下载视频片段
# 5. 下载秘钥，进行解密
# 6. 合并所有ts文件为一个视频文件



import requests
import base64
import json
from bs4 import BeautifulSoup
import aiofiles
import aiohttp
import asyncio
from Crypto.Cipher import AES
import os



# 获取m3u8入口文件地址
def get_index_m3u8_url(url):
  res = requests.get(url)
  res.encoding = "utf-8"
  # print(res.text)

  soup = BeautifulSoup(res.text, 'lxml')
  ele = soup.select('iframe')[0]
  print(ele['data-play'])
  b64_str = soup.select('iframe')[0]['data-play']
  # b64_str = 'NQfZXlKMWNtd2lPaUpvZEhSd2N6cGNMMXd2ZGk1Mk1XdGtMbU52YlZ3dk1qQXlNakExTURsY0x6bGtTMGwzYUhWRlhDOXBibVJsZUM1dE0zVTRJaXdpY0d4aGVXbGtJam9pZDNkM0xtdHdhM1ZoYm1jdVpHVmZOVEl4TkRFNVh6SWlMQ0p1WlhoMElqb2lYQzkyYjJSd2JHRjVYQzgxTWpFME1Ua3RNaTB6TG1oMGJXd2lMQ0p3YVdNaU9pSmNMM1Z3Ykc5aFpGd3ZkbTlrWEM4eU1ESXlNRFF5TlMweFhDOWhabUpsT0RCa09EQmhOVEZrWmpBMU1HVmhOMk16TldZNU1EVXhNelF5WkM1cWNHY2lmUT09'
  # 注意该字符串需要去除前3位字符，否则base64解码会有问题
  b64_str = b64_str[3:]
  # print(b64_str)
  # remainder = len(b64_str) % 3
  # # if(remainder != 0):
  # #   b64_str = b64_str + ('=' * remainder)
  # b64_str = b64_str + ('=' * remainder)
  
  # 需要进行2次base64解码才能获取到index地址参数
  temp_str = base64.b64decode(b64_str).decode('utf-8')
  # print(base64.b64decode(temp_str).decode('utf-8'))
  obj_str = base64.b64decode(temp_str).decode('utf-8')
  # print(json.loads(obj_str)['url'])
  index_url = json.loads(obj_str)['url']
  return index_url


# 获取解密视频需要的key
def get_key(url):
  # headers={
  #   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
  # }
  res = requests.get(url=url)
  print(res.text)
  return res.text


# 下载m3u8文件并保存
def download_m3u8_txt(url, file_name):
  res = requests.get(url)
  with open(file_name, mode='wb') as f:
    f.write(res.content)


# 下载ts文件片段并保存
async def download_ts(ts_url, line, session):
  # 注意此处ts文件名称带有前缀，作为文件名时需要进行处理
  ts_name = line.rsplit('/', 1)[1]
  async with session.get(url=ts_url) as res:
    async with aiofiles.open(f'video_ts/{ts_name}', mode="wb") as f:
      await f.write(await res.content.read())
  print(ts_name, 'download finish')


# 创建异步下载队列
async def aio_dl_task(base_url, list_file_name):
  tasks = []
  async with aiofiles.open(list_file_name, mode='r', encoding='utf-8') as f:
    async with aiohttp.ClientSession() as session:
      async for line in f:
        if line.startswith('#'):
          continue
        line = line.strip()
        ts_url = base_url + line
        print(ts_url)
        c = asyncio.create_task(download_ts(ts_url, line, session))
        tasks.append(c)
      await asyncio.wait(tasks)


# 加密ts文件解密
async def decrypt_ts(line, ts_key):
  # 注意此处ts文件名称带有前缀，作为文件名时需要进行处理
  ts_name = line.rsplit('/', 1)[1]
  aes_dec = AES.new(key=ts_key.encode('utf-8'), mode=AES.MODE_CBC, iv=b'0123456789123456')
  async with aiofiles.open(f'video_ts/{ts_name}', mode="rb") as ori_f, aiofiles.open(f'video_decrypt/temp_{ts_name}', mode="wb") as res_f:
    # 从源文件读取加密ts文件内容
    temp_b = await ori_f.read()
    # 解密后把数据写入文件
    await res_f.write(aes_dec.decrypt(temp_b))
  print(f'{ts_name} decrypt finish')


# 创建异步解密队列
async def aio_dec_task(list_file_name, key):
  tasks = []
  async with aiofiles.open(list_file_name, mode='r', encoding='utf-8') as f:
    async for line in f:
      if line.startswith('#'):
        continue
      line = line.strip()
      c = asyncio.create_task(decrypt_ts(line, key))
      tasks.append(c)
  await asyncio.wait(tasks)


# 合并解密后的ts文件
def merge_ts(list_file_name):
  merge_list_file = 'merge_ts_names_list.txt'
  path ='./video_decrypt'
  list = []
  with open(list_file_name, mode='r', encoding='utf-8') as f:
    for line in f:
      if line.startswith('#'):
        continue
      line = line.strip() # /20220509/9dKIwhuE/2000kb/hls/MxEtfW4o.ts
      # 注意此处ts文件名称带有前缀，作为文件名时需要进行处理
      ts_name = line.rsplit('/', 1)[1]
      list.append(ts_name)
  with open(merge_list_file, mode = 'w', encoding='utf-8') as f:
    for item in list:
      f.write(f"file {path}/temp_{item}\n")
  output_file_name = 'TMWFTE_02.mp4'
  cmd_str = f"ffmpeg -f concat -safe 0 -i {merge_list_file} -c copy {output_file_name}"
  print(cmd_str)
  try:
    # 执行合并命令
    os.system(cmd_str)
  except Exception as e:
      print(e)
  print("merge finish")


def main():
  page_url = 'https://www.kpkuang.de/vodplay/521419-2-2.html'
  # 获取入口m3u8文件地址
  index_url = get_index_m3u8_url(page_url)
  # index_url = 'https://v.v1kd.com/20220509/9dKIwhuE/index.m3u8'
  # 入口（第一层）m3u8文件名
  index_file_name = 'index_m3u8.txt'
  # 列表（第二层）m3u8文件名
  list_file_name = 'list_m3u8.txt'
  # 下载入口m3u8文件
  download_m3u8_txt(index_url, index_file_name)
  # 获取列表m3u8文件地址
  with open(index_file_name, mode='r', encoding='utf-8') as f:
    for line in f:
      if line.startswith('#'):
        continue
      line = line.strip()
      # 处理地址，获得文件地址前缀
      temp_url = index_url.split('//')[1].split('/')[0]
      # 之前为了方便拆分去除了地址协议前缀，需要重新加上
      base_url = 'https://' + temp_url # https://v.v1kd.com
      # 拼接列表文件地址
      list_m3u8_url = base_url + line # https://v.v1kd.com/20220509/9dKIwhuE/2000kb/hls/index.m3u8
  # print(list_m3u8_url)
  # 下载列表m3u8文件
  download_m3u8_txt(list_m3u8_url, list_file_name)
  asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  # 下载ts视频片段文件
  asyncio.run(aio_dl_task(base_url, list_file_name))
  # 从列表m3u8文件中，拼接获取ts解密key地址
  with open(list_file_name, mode='r', encoding='utf-8') as f:
    for line in f:
      if line.find('URI=') != -1:
        print(line) # #EXT-X-KEY:METHOD=AES-128,URI="/20220509/9dKIwhuE/2000kb/hls/key.key"
        # 注意此处需要去除双引号"
        temp = line.split('URI="')[1].strip()
        key_url = base_url + temp[:-1] # https://v.v1kd.com/20220509/9dKIwhuE/2000kb/hls/key.key
        break
  print(key_url)
  # 获取ts解密key
  ts_key = get_key(key_url)
  # 解密视频，生成可直接播放的ts片段
  asyncio.run(aio_dec_task(list_file_name, ts_key))
  # 合并解密后的ts文件
  merge_ts(list_file_name)




if __name__ == '__main__':
  main()