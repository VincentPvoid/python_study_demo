import scrapy
import json

class BdfanyiSpider(scrapy.Spider):
    name = 'bdfanyi'
    allowed_domains = ['https://fanyi.baidu.com/sug']
    # post请求必须传递参数
    # 所以用不上start_urls和parse方法
    # start_urls = ['https://fanyi.baidu.com/sug/']
    # def parse(self, response):
    #     pass


    def start_requests(self):
        # return super().start_requests()
        url = 'https://fanyi.baidu.com/sug'
        data = {
          'kw':'journey'
        }
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse_second)

    def parse_second(self, response):
      content = response.text
      obj = json.loads(content)
      print(obj)