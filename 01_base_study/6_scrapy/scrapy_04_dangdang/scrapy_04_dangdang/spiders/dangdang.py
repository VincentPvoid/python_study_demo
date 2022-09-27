import scrapy
from scrapy_04_dangdang.items import Scrapy04DangdangItem


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    # 如果需要进行多页爬取，则需要调整allowed_domains的范围；一般情况下只写目标网址的域名
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.54.92.01.00.00.html']

    base_url = 'http://category.dangdang.com/pg'
    page = 1

    def parse(self, response):
      # pipelines  下载数据
      # items  定义数据结构

      # print('===============')
      # 图片 src = //div[@id='search_nature_rg']//li//img/@src
      # 书名 title = //div[@id='search_nature_rg']//li//img/@alt
      # 价格 price = //div[@id='search_nature_rg']//li//span[@class='search_now_price']/text()

      lis_list = response.xpath("//div[@id='search_nature_rg']//li")
      # 所有的Selector对象，都可以再次调用xpath方法

      for li in lis_list:
        # 图片使用了懒加载，因此需要使用data-original属性取值
        src = li.xpath(".//img/@data-original").extract_first()
        # 但已经加载的图片（一般为第一张图片）没有data-original，因此需要进行判断
        if src:
          src = src
        else:
          src = li.xpath(".//img/@src").extract_first()


        src = 'http:' + src
        title = li.xpath(".//img/@alt").extract_first()
        price = li.xpath(".//span[@class='search_now_price']/text()").extract_first()

        # print(src, title, price)
        book = Scrapy04DangdangItem(src=src, title=title, price=price)

        # 获取一个数据对象就将改对象交给pipelines
        yield book

        if(self.page < 5):
          self.page = self.page +1
          url = self.base_url + str(self.page) + '-cp01.54.92.01.00.00.html'

          # 调用parse方法
          # scrapy.Request就是scrapy的get请求
          # 参数callback表示要执行的回调函数
          yield scrapy.Request(url=url, callback=self.parse)


