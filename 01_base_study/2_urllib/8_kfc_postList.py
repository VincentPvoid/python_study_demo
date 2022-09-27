# https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname
# data = {
#   cname: 北京
#   pid: 
#   pageIndex: 1
#   pageSize: 10
# }



# 爬取KFC官网店铺数据



import urllib.parse
import urllib.request

# 请求对象的定制
def create_request(page):
  BASE_URL = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
  }
  data = {
    'cname': '北京',
    'pid': '',
    'pageIndex': page,
    'pageSize': 10,
  }
  data = urllib.parse.urlencode(data).encode('utf-8')
  request = urllib.request.Request(url=BASE_URL, data=data, headers=headers)
  return request

# 获取网页响应内容
def get_res_content(request):
  content = urllib.request.urlopen(request).read().decode('utf-8')
  return content

# 下载内容并保存为文件
def download_data(page, content):
  with open('./kfcData/kfc_' + str(page) + '.json', 'w', encoding='utf-8') as fp:
    fp.write(content)



if __name__ == '__main__':
  start_page = int(input('please input start page: '))
  end_page = int(input('please input end page: '))
  for page in range(start_page, end_page+1):
    request = create_request(page)
    content = get_res_content(request)
    download_data(page, content)
