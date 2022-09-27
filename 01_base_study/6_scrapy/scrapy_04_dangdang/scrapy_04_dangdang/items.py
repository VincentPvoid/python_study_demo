# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy04DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 需要下载的数据结构
    
    # 图片地址
    src = scrapy.Field()
    # 书名
    title = scrapy.Field()
    # 价格
    price = scrapy.Field()
