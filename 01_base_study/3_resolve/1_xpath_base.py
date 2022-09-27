# 需要先添加库的路径，否则无法引入lxml库
# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

from lxml import etree

# etree.parse() 解析本地文件
# html_tree = etree.parse('XX.html')
# etree.HTML() 服务器响应文件
# html_tree = etree.HTML(response.read().decode('utf‐8')

# xpath解析本地文件
# 如果该html文件的标签没有闭合会报错（meta标签没有结束标签/)
# lxml.etree.XMLSyntaxError: Opening and ending tag mismatch: meta line 5 and head, line 8, column 8
tree = etree.parse('./testData/lxml_base_test.html')

# 1.路径查询
# //：查找所有子孙节点，不考虑层级关系
# / ：找直接子节点

# 查找ul下面的li
# li_list = tree.xpath('//body/ul/li')


# 2.谓词查询
# //div[@id]
# //div[@id="maincontent"]


# 查找所有有id属性的li标签
# 内容查询 test()获取标签的内容
# //div/h1/text() 
# li_list = tree.xpath('//body/ul/li[@id]/text()')

# 查找id为hunter1的标签（注意引号）
# li_list = tree.xpath('//body/ul/li[@id="hunter1"]/text()')


# 3.属性查询
# //@class
# 获取id为hunter1的标签的class值
# li_list = tree.xpath('//body/ul/li[@id="hunter1"]/@class')



# 4.模糊查询
# //div[contains(@id, "he")]
# //div[starts‐with(@id, "he")]

# 查找id包含hunter字段的标签
# li_list = tree.xpath('//ul/li[contains(@id, "hunter")]/text()')

# 查找class中以old开头的标签
# li_list = tree.xpath('//ul/li[starts-with(@class, "old")]/text()')


# 5.逻辑运算
# //div[@id="head" and @class="s_down"]
# //title | //price

# 查找开头为hunter并且class值为old-hunter的标签
li_list = tree.xpath('//ul/li[starts-with(@id,"hunter") and @class="old-hunter"]/text()')
# 查找id为hunter1或hunter2的标签
# li_list = tree.xpath('//ul/li[@id="hunter1"]/text() | //ul/li[@id="hunter2"]/text()')


print(li_list)