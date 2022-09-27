import sys
sys.path.append("D:\Python\Python310\Lib\site-packages")

# 服务器响应的文件生成对象
# soup = BeautifulSoup(response.read().decode(), 'lxml')
# 本地文件生成对象
# soup = BeautifulSoup(open('1.html'), 'lxml')
# 注意：默认打开文件的编码格式gbk所以需要指定打开编码格式

from bs4 import BeautifulSoup


# 通过解析本地文件来认识bs4的基础语法
# 默认打开文件的编码为gbk，所以在打开文件夹时需要指定编码
soup = BeautifulSoup(open('./testData/lxml_base_test.html', encoding='utf-8'), 'lxml')

# print(soup)

# 根据标签名查找节点
# 注意：返回的是第一个符合条件的数据；与js中数组的find()类似
# print(soup.a)
# 获取标签的属性和属性值（以对象的格式返回）
# print(soup.a.attrs)



# bs4的一些常用函数

# 1. find()
# 返回的是第一个符合条件的数据；与js中数组的find()类似
# print(soup.find('a'))

# 找到title为company的a标签
# print(soup.find('a', title="company"))

# 找到class为doll的第一个li标签
# 注意class的写法，需要写为class_
# print(soup.find('li', class_="doll"))



# 2. find_all()
# 返回值为一个列表（数组），如果没有符合条件的值则返回[]；与js中数组的filter()类似
# print(soup.find_all('input'))
# print(soup.find_all('a'))

# 注意：当想获取多个不同的标签时，需要写为列表的形式
# print(soup.find_all(['a', 'li']))

# 如果加上limit参数，则表示获取所有对应值的前n个数据
# print(soup.find_all('li', limit=2))



# 3. select() 较为推荐的方法；类似于js中的document.querySelectorAll()
# 返回值为一个列表（数组），如果没有符合条件的值则返回[]
# print(soup.select('.old-hunter'))
# print(soup.select('#hunter1'))

# 属性选择器：通过属性来获取对应的标签
# 获取li中有id的标签
# print(soup.select('li[id]'))
# print(soup.select('li[id="hunter2"]'))


# 层级选择器；与css中的选择器类似
# 获取body下的所有a标签
# print(soup.select('body a'))

# 子元素选择器
# 获取body下的子a标签，不包括后代a标签
# 注意：在很多的计算机编程语言中 ，>等符号前后不加空格会报错；但在bs4中，空格可加可不加
# print(soup.select('body>a'))

# 找到所有的a标签和li标签
# print(soup.select('a, li'))


# 获取节点内容
# 如果获取到的标签中只含有文本节点，则string和get_text()方法都可以使用；如果包含子元素，则只能使用get_text()
# 一般情况下，更常用get_text()
# obj = soup.select('#test-list')[0]
# print(obj.string) # None
# print(obj.get_text())

# obj = soup.select('#hunter1')[0]
# print(obj.string) 
# print(obj.get_text())


# 节点的属性
obj = soup.select('#hunter1')[0]

# name返回标签的名称
# print(obj.name)

# 获取标签的属性和属性值（以对象的格式返回）；注意class对应的值是数组的格式
# print(obj.attrs)

# 获取节点的类名；注意返回值都为数组格式
print(obj.attrs.get('class'))
print(obj.get('class'))
print(obj['class'])




