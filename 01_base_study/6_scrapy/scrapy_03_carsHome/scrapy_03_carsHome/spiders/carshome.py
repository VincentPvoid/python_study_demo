import scrapy


class CarshomeSpider(scrapy.Spider):
    name = 'carshome'
    allowed_domains = ['https://car.autohome.com.cn/price/brand-36.html']
    # 注意：如果请求接口以.html为结尾，则不要加/，否则会报错
    start_urls = ['https://car.autohome.com.cn/price/brand-36.html']

    def parse(self, response):
        car_names_list = response.xpath("//div[@id='brandtab-1']//div[@class='main-title']/a/text()")
        price_list = response.xpath("//div[@id='brandtab-1']//div[@class='main-lever-right']//span[@class='font-arial']/text()")

        print('======================')
        # print(car_names_list)

        # for car_name in car_names_list:
        #   print(car_name.extract())

        for i in range(len(car_names_list)):
          car_name = car_names_list[i].extract()
          price = price_list[i].extract()
          print(car_name, price)


