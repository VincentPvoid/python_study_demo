import scrapy
from scrapy_05_movie.items import Scrapy05MovieItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.dy2018.com']
    start_urls = ['https://www.dy2018.com/16/']

    def parse(self, response):
        # //div[@class='co_area2']//div[@class='co_content8']//a[@class='ulink'][2]

        as_list = response.xpath("//div[@class='co_area2']//div[@class='co_content8']//a[@class='ulink'][2]")
        
        for a in as_list:
          # 获取第一页的电影名称和要跳转的链接地址
          name = a.xpath('./@title').extract_first()
          href = a.xpath('./@href').extract_first()
          # print(name, href)

          # 拼接需要跳转的地址
          url = 'https://www.dy2018.com/' + href

          # 对链接发起访问
          yield scrapy.Request(url=url, callback=self.parse_second, meta={'name':name})

     
    def parse_second(self, response):
      # print('aaaaaaaaaaaaa')
      # //div[@id='Zoom']/img[1]/@src

      # 注意：如果拿不到数据，应该检查一下xpath语法是否正确
      src = response.xpath("//div[@id='Zoom']/img[1]/@src").extract_first()
      # 可以使用meta参数传值
      name = response.meta['name']

      movie = Scrapy05MovieItem(name=name, src=src)

      yield movie
      



