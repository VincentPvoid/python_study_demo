# 下载 站长素材 站内的图片
# 该例子中有重复文件名，因此数量可能不足

import sys
sys.path.append("D:\Python\Python310\Lib\site-packages")

import urllib.request
from lxml import etree


# 请求对象的定制
def create_request(page):
  if(page==1):
    url = 'https://sc.chinaz.com/tupian/dahaitupian.html'
  else:
    url = 'https://sc.chinaz.com/tupian/dahaitupian_' + str(page) +'.html'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
  }
  request = urllib.request.Request(url=url, headers=headers)
  return request

# 获取网页响应内容
def get_res_content(request):
  response = urllib.request.urlopen(request)
  content = response.read().decode('utf-8')
  return content

def download_imgs(content):
  tree = etree.HTML(content)
  img_src_list = tree.xpath('//div[@id="container"]/div/div//img/@src2')
  # print(img_src_list)
  title_list = tree.xpath('//div[@id="container"]/div/div//img/@alt')
  # print(title_list)
  for i in range(len(img_src_list)):
    img_title = title_list[i]
    img_url = 'https:' + img_src_list[i]
    # print(img_title, img_url)
    urllib.request.urlretrieve(url = img_url, filename = img_title + '.jpg')


if __name__ == '__main__':
  start_page = int(input('please input start page: '))
  end_page = int(input('please input end page: '))
  for page in range(start_page, end_page+1):
    request = create_request(page)
    content = get_res_content(request)
    download_imgs(content)