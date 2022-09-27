import urllib.request
import urllib.parse
# 下载前10页数据
# 下载的步骤：1.请求对象的定制 2.获取响应的数据 3.下载
# 每执行一次返回一个request对象
def create_request(page):
  base_url = 'https://movie.douban.com/j/chart/top_list?type=20&interval_id=100%3A90&action=&'
  headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/76.0.3809.100 Safari/537.36'
  }
  data={
  #  1 2 3 4
  # 0 20 40 60
    'start': (page-1)*20,
    'limit': 20
  }
  # data编码
  data = urllib.parse.urlencode(data)
  url = base_url + data
  request = urllib.request.Request(url=url,headers=headers)
  return request

# 获取网页源码
def get_content(request):
  response = urllib.request.urlopen(request)
  content = response.read().decode('utf-8')
  return content

def down_load(page,content):
  # with open（文件的名字，模式，编码）as fp:
  # fp.write(内容)
  with open('douban_'+str(page)+'.json','w',encoding='utf-8')as fp:
    fp.write(content)


if __name__ == '__main__':
  start_page = int(input('请输入起始页码'))
  end_page = int(input('请输入结束页码'))
  for page in range(start_page,end_page+1):
    request = create_request(page)
    content = get_content(request)
    down_load(page,content)