# 基础

1. 创建爬虫项目 scrapy startproject 项目名称
注意： 项目名称不能用数字开头，也不能包含中文

2. 创建爬虫文件
需要在spiders文件夹中创建爬虫文件
进入该文件夹中创建爬虫文件
scrapy genspider 爬虫文件名称 要爬取的网页名称（一般情况下前面不需要添加http等协议名称）
例 scrapy genspider baidu www.baidu.com

3. 运行爬虫代码
scrapy crawl 爬虫的名称
例 scrapy crawl baidu




# 项目结构

## scrapy项目结构
项目名称
  项目名称
    spiders文件夹
    __init__.py
    自定义的爬虫文件.py ‐‐‐》由我们自己创建，爬虫核心功能文件
    __init__.py
    items.py  ‐‐‐》定义数据结构的地方，爬取的数据包含的内容，是一个继承自scrapy.Item的类
    middlewares.py  ‐‐‐》中间件 代理
    pipelines.py  ‐‐‐》管道文件，里面只有一个类，用于进行下载数据的后续处理；默认是300优先级，值越小优先级越高（1‐1000）
    settings.py   ‐‐‐》配置文件 比如：是否遵守robots协议，User‐Agent定义等


## response的属性和方法
response.text       ‐‐‐》以字符串的形式返回响应内容
response.body       ‐‐‐》以二进制的形式返回响应内容
response.xpath()    --‐》可以直接使用xpath的语法解析响应内容（注意返回值都是列表形式）
response.extract()  ‐‐‐》提取selector对象的data属性值
response.extract_first()    ‐‐‐》提取selector列表中的第一个数据



# scrapy架构组成

1. 引擎
‐‐‐》自动运行，无需关注，会自动组织所有的请求对象，分发给下载器
2. 下载器
‐‐‐》从引擎处获取到请求对象后，请求数据
3. spiders
‐‐‐》Spider类定义了如何爬取某个(或某些)网站。包括了爬取的动作(例
如:是否跟进链接)以及如何从网页的内容中提取结构化数据(爬取item)。 换句话说，Spider就是您定义爬取的动作及
分析某个网页(或者是有些网页)的地方。
4. 调度器
‐‐‐》有自己的调度规则，无需关注
5. 管道（Item pipeline） ‐‐‐》最终处理数据的管道，会预留接口供我们处理数据
当Item在Spider中被收集之后，它将会被传递到Item Pipeline，一些组件会按照一定的顺序执行对Item的处理。
每个item pipeline组件(有时称之为“Item Pipeline”)是实现了简单方法的Python类。他们接收到Item并通过它执行
一些行为，同时也决定此Item是否继续通过pipeline，或是被丢弃而不再进行处理。

以下是item pipeline的一些典型应用：
- 清理HTML数据
- 验证爬取的数据(检查item包含某些字段)
- 查重(并丢弃)
- 将爬取结果保存到数据库中



# scrapy shell
Scrapy终端，是一个交互终端，供您在未启动spider的情况下尝试及调试您的爬取代码。 其本意是用来测试提取
数据的代码，不过您可以将其作为正常的Python终端，在上面测试任何的Python代码。

注意：
  使用时直接在命令行中输入 scrapy shell 目标url
  不需要进入python或是ipython中


# CrawlSpider
scrapy.linkextractors.LinkExtractor(
  allow = (), # 正则表达式 提取符合正则的链接
  deny = (), # (不用)正则表达式 不提取符合正则的链接
  allow_domains = (), # （不用）允许的域名
  deny_domains = (), # （不用）不允许的域名
  restrict_xpaths = (), # xpath，提取符合xpath规则的链接
  restrict_css = () # 提取符合选择器规则的链接
)

例
正则用法：links1 = LinkExtractor(allow=r'list_23_\d+\.html')
xpath用法：links2 = LinkExtractor(restrict_xpaths=r'//div[@class="x"]')
css用法：links3 = LinkExtractor(restrict_css='.x')

## 提取链接
link.extract_links(response)

## 读书网数据入库
1. 创建项目：scrapy startproject 项目名称
2. 跳转到spiders路径 cd\dushuproject\dushuproject\spiders
3. 创建爬虫类：scrapy genspider ‐t crawl read 爬取地址
4. items
5. spiders
6. settings
7. pipelines
数据保存到本地
数据保存到mysql数据库



# 日志
日志信息和日志等级

## 日志级别
CRITICAL：严重错误
ERROR： 一般错误
WARNING： 警告
INFO: 一般信息
DEBUG： 调试信息

严重程度从高到低排列
默认的日志等级为DEBUG
如果出现了DEBUG或者DEBUG以上等级的日志
就会打印相关日志
可以在settings文件中进行相关设置

## settings.py设置
LOG_FILE : 将屏幕显示的信息全部记录到文件中，屏幕不再显示，注意文件后缀是.log
LOG_LEVEL : 设置日志显示的等级；一般不进行调整（默认DEBUG）
