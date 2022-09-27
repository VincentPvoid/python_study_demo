import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_06_dushu.items import Scrapy06DushuItem


class DushuSpider(CrawlSpider):
    name = 'dushu'
    allowed_domains = ['www.dushu.com']
    # 注意开始链接地址要包含第一页，否则爬取会缺失第一页数据
    start_urls = ['https://www.dushu.com/book/1107_1.html']

    # follow参数表示是否按照规则继续进行爬取
    rules = (
        Rule(LinkExtractor(allow=r'/book/1107_\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print('++++++++++++++++++++++=')

        # //div[@class='bookslist']//li//img
        imgs_list = response.xpath("//div[@class='bookslist']//li//img")

        for img in imgs_list:
          name = img.xpath('./@alt').extract_first()
          src = img.xpath('./@data-original').extract_first()

          if(src):
            src = src
          else:
            src = img.xpath('./@src').extract_first()
          
          # print(name, src)
          book = Scrapy06DushuItem(name=name, src=src)

          yield book

        

        # return item
