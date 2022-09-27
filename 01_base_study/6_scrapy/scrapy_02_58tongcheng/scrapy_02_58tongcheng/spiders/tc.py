import scrapy


class TcSpider(scrapy.Spider):
    name = 'tc'
    allowed_domains = ['https://bj.58.com/job/?key=%E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88']
    start_urls = ['https://bj.58.com/job/?key=%E6%B5%8B%E8%AF%95%E5%B7%A5%E7%A8%8B%E5%B8%88/']

    def parse(self, response):
        # 以字符串的形式返回响应内容
        # content = response.text

        # 以二进制的形式返回响应内容
        # content = response.body

        span = response.xpath("/html/body//div[@class='list_head']/div/span")[0]

        print('=========================')
        # print(content)

        print(span.extract())
