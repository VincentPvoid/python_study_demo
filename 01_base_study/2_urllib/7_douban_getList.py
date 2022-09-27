
# https://movie.douban.com/j/chart/top_list?type=17&interval_id=100%3A90&action=&start=0&limit=20
# https://movie.douban.com/j/chart/top_list?type=17&interval_id=100%3A90&action=&start=20&limit=20
# https://movie.douban.com/j/chart/top_list?type=17&interval_id=100%3A90&action=&start=40&limit=20


# 爬取豆瓣电影前n页数据
# 下载的步骤：1.请求对象的定制 2.获取响应的数据 3.下载（保存为文件）

import urllib.request
import urllib.parse


# 自定义请求对象函数
def create_request(page):
  BASE_URL = 'https://movie.douban.com/j/chart/top_list?type=17&interval_id=100%3A90&action=&limit=20&'
  data = {
    'start':(page-1)*20
  }
  data = urllib.parse.urlencode(data)
  url = BASE_URL + data
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
  }

  request = urllib.request.Request(url=url, headers=headers)
  return request

# 发送请求并返回响应函数
def get_content(request):
  response = urllib.request.urlopen(request)
  content = response.read().decode('utf-8')
  return content

# 把获取到的json内容保存为文件
def download_data(page,content):
  # open方法默认情况下使用的是gbk编码，因此如果想要保存汉字，需要在open方法中指定编码格式的参数为utf-8
  # 注意参数中的page为int，和str拼接时需要转换为str才能进行拼接；这点与js不同

  # encoding = 'utf-8'
  # fp = open('douban.json','w',encoding=encoding)
  # fp.write(content)
  
  # 上面的代码可以简化为下面的代码
  # with open（文件的名字，模式，编码）as fp:
  #   fp.write(内容)
  encoding = 'utf-8'
  with open('./doubanData/douban'+ str(page) + '.json', 'w', encoding=encoding) as fp:
    fp.write(content)



# 一个python文件通常有两种使用方法
# 第一是作为脚本直接执行，第二是 import 到其他的 python 脚本中被调用（模块重用）执行。
# 因此 if __name__ == 'main': 的作用就是控制这两种情况执行代码的过程，
# 在 if __name__ == 'main': 下的代码只有在第一种情况下（即文件作为脚本直接执行）才会被执行，而 import 到其他脚本中是不会被执行的
if __name__ == '__main__':
  start_page = int(input('please input start page: '))
  end_page = int(input('please input end page: '))
  for page in range(start_page, end_page+1):
    request = create_request(page)
    content = get_content(request)
    download_data(page,content)

