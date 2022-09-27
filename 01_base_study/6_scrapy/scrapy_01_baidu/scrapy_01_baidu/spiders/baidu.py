import scrapy


class BaiduSpider(scrapy.Spider):
    # 爬虫的名称
    name = 'baidu'
    # 允许访问的域名 爬取时，如果不是此域名之下的url会被过滤
    allowed_domains = ['www.baidu.com']
    # 起始url地址（第一次访问的域名）可以写多个url，一般是一个
    # start_urls会自动在allowed_domains前面添加协议，后面添加/
    start_urls = ['http://www.baidu.com/']

    # 解析数据的回调函数；response就是返回的响应对象
    def parse(self, response):
      print('test AAAAAAAAA')
        # pass
