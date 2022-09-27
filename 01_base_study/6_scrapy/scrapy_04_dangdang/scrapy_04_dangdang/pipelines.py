# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import urllib.request

# 使用管道时，需要在settings中先开启
class Scrapy04DangdangPipeline:

    # 在爬虫开始前执行的方法
    def open_spider(self, spider):
      # print('+++++++++++++++++++++')
      self.fp = open('books.json', 'w', encoding='utf-8')


    # item就是yield接收到的目标数据对象
    def process_item(self, item, spider):
      # 不推荐使用以下模式，因为会对文件进行频繁的读写操作
      # write方法写入的是字符串，不能是其他对象
      # with open('books.json', 'a', encoding='utf-8')as fp:
      #   fp.write(str(item))

      self.fp.write(str(item))

      return item


    # 在爬虫结束后执行的方法
    def close_spider(self, spider):
      # print('-----------------------')
      self.fp.close()


# 开启其他管道
# 1. 定义管道类
# 2. 在settings中开启管道
# 'scrapy_04_dangdang.pipelines.DangDangDownloadPipeline': 301
class DangDangDownloadPipeline:
  def process_item(self, item, spider):

    url = item.get('src')
    title = './books/' +item.get('title') + '.jpg'
    
    urllib.request.urlretrieve(url=url, filename=title)

    return item
