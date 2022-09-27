# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")



# selenium的使用步骤
# （1）导入：from selenium import webdriver
# （2）创建谷歌浏览器操作对象：
# path = 谷歌浏览器驱动文件路径
# browser = webdriver.Chrome(path)
# （3）访问网址
# url = 要访问的网址
# browser.get(url)


# 1. 导入selenium
from selenium import webdriver

# 2. 创建浏览器操作对象
path = 'chromedriver.exe'
browser = webdriver.Chrome(path)

# 3. 访问网站
url = 'https://www.baidu.com'
browser.get(url)