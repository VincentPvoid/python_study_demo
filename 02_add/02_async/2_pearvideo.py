# 爬取梨视频

# 视频目标地址
# https://www.pearvideo.com/videoStatus.jsp

# get请求参数
# contId: 1753858 视频id
# mrd: 0.16300018305020303 随机数

# 视频真实地址
# 该请求返回的对象中的videoInfo.videos.srcUrl
# 例 https://video.pearvideo.com/mp4/adshort/20220309/1646840725597-15837074_adpkg-ad_hd.mp4
# 把-15837074前面的数字替换为cont-1753858（cout- + id）就是视频的真实地址
# https://video.pearvideo.com/mp4/adshort/20220309/cont-1753858-15837074_adpkg-ad_hd.mp4


import requests
from lxml import etree
import random
from multiprocessing.dummy import Pool


url = 'https://www.pearvideo.com/category_8'

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

response = requests.get(url=url, headers=headers)

content = response.text
# print(content)
tree = etree.HTML(content)

div_list = tree.xpath("//div[@class='vervideo-bd']")
# print(res)

# 发送请求获取视频地址
def get_video_data_url(video_id):
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    # 需要根据视频id添加referer，否则返回无法返回正确响应（会显示该文章已下线）
    'Referer': 'https://www.pearvideo.com/' + 'video_' + video_id
  }
  url_video = 'https://www.pearvideo.com/videoStatus.jsp'
  data = {
    'contId': video_id,
    'mrd': random.random()
  }
  response = requests.get(url=url_video, params=data, headers=headers)
  # 把返回的响应转换为json格式（方便取值）
  content_obj = response.json()
  # print(content_obj)
  # 获取到返回的视频地址；但还需要进行处理才能得到真实地址
  srcUrl = content_obj['videoInfo']['videos']['srcUrl']
  # print(srcUrl)
  real_url = handle_real_url(srcUrl, video_id)
  # print(real_url)
  return real_url



# 根据返回的视频地址url，处理后获取真实视频地址
# 原地址 https://video.pearvideo.com/mp4/third/20220308/1646905610129-10037564-183251-hd.mp4
# 真实地址 https://video.pearvideo.com/mp4/third/20220308/cont-1753775-10037564-183251-hd.mp4
def handle_real_url(srcUrl, video_id):
  # 根据/拆分字符串
  strArr = srcUrl.split('/')
  # 最后一段1646905610129-10037564-183251-hd.mp4，再次根据-进行拆分
  tempArr = strArr[len(strArr)-1].split('-')
  # 拆分后第一段1646905610129替换为'cont-' + video_id
  tempArr[0] = 'cont-' + video_id
  # 用-拼接最后一段cont-1753775-10037564-183251-hd.mp4
  temp = '-'.join(tempArr)
  # 把一开始拆分的数组的最后一位替换为拼接完的temp字符串
  strArr[len(strArr)-1] = temp
  # 用/拼接字符串数组
  return '/'.join(strArr)
  # print('/'.join(strArr))

# 对视频链接发起请求获取视频的二进制数据
def download_video(dicObj):
  url = dicObj['url']
  print(dicObj['name']+' is downloading...')
  # 以二进制字节的形式返回网页源码
  data = requests.get(url=url, headers=headers).content
  # 持久化存储
  with open('./pearlVideos/' + dicObj['name'] + '.mp4', 'wb') as fp:
    fp.write(data)
    print(dicObj['name']+' download finished')


# 存储所有的视频地址和名称（结构{name:xxx, url:xxx,}）
dic_list = []

for div in div_list:
  video_name = div.xpath(".//div[@class='vervideo-title']/text()")[0]
  a_href = div.xpath('./a/@href')[0]
  # 获取视频id参数
  video_id = a_href.split('_')[1]
  # print(video_id, video_name)
  url = get_video_data_url(video_id)
  dic = {
    'name': video_name,
    'url': url,
  }
  dic_list.append(dic)
  # break

# print(dic_list)

# 使用线程池对视频数据进行请求（较为耗时的阻塞操作）
pool = Pool(5)
pool.map(download_video, dic_list)

# 关闭pool，使其不再接受新的（主进程）任务
pool.close()
# 等待子进程运行完后，再把主进程全部关掉
pool.join()
