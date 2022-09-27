# 例：bs4爬取星巴克数据

import sys
sys.path.append("D:\Python\Python310\Lib\site-packages")

import urllib.request
from bs4 import BeautifulSoup


url = 'https://www.starbucks.com.cn/menu/'
response = urllib.request.urlopen(url)
content = response.read().decode('utf-8')
# print(content)

soup = BeautifulSoup(content, 'lxml')

# 产品名称
# //ul[@class="grid padded-3 product"]//strong/text()
# product_list = soup.select('ul[class="grid padded-3 product"] strong')
product_list = soup.select('.grid.padded-3.product strong')

# print(product_list)
# for product in product_list:
#   print(product.get_text())

# 产品图片
# //ul[@class="grid padded-3 product"]//div[@class="preview circle"]/@style
imgs_list = soup.select('.grid.padded-3.product div.preview.circle')
# print(imgs_list)
# print(imgs_list[0].attrs['style'].split('url(')[1].split(')')[0], type(imgs_list[0].attrs['style']))
for i in range(len(imgs_list)):
  url = imgs_list[i].attrs['style'].split('url("')[1].split('")')[0]
  url = 'https://www.starbucks.com.cn' + url
  # print(url)
  img_title = product_list[i].get_text().replace('/','_')
  # print(url, img_title)
  try:
    urllib.request.urlretrieve(url = url, filename= str(i) + '_' + img_title + '.jpg')
  except urllib.error.ContentTooShortError:
    print(url, img_title)




# 整合为一个下载函数
def download_imgs(content):
  soup = BeautifulSoup(content, 'lxml')
  product_list = soup.select('.grid.padded-3.product strong')
  imgs_list = soup.select('.grid.padded-3.product div.preview.circle')
  for i in range(len(imgs_list)):
    url = imgs_list[i].attrs['style'].split('url("')[1].split('")')[0]
    url = 'https://www.starbucks.com.cn' + url
    # print(url)
    img_title = product_list[i].get_text()
    try:
      urllib.request.urlretrieve(url = url, filename= str(i) + '_' + img_title + '.jpg')
    except urllib.error.ContentTooShortError:
      print(url, img_title)