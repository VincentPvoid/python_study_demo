# selenium的元素定位
# 元素定位：自动化要做的就是模拟鼠标和键盘来操作来操作这些元素，点击、输入等等。操作这些元素前首先
# 要找到它们，WebDriver提供很多定位元素的方法
# 方法：
# 1.find_element_by_id
# eg:button = browserfind_element_by_id('su')
# 2.find_elements_by_name
# eg:name = browserfind_element_by_name('wd')
# 3.find_elements_by_xpath
# eg:xpath1 = browserfind_elements_by_xpath('//input[@id="su"]')
# 4.find_elements_by_tag_name
# eg:names = browserfind_elements_by_tag_name('input')
# 5.find_elements_by_css_selector
# eg:my_input = browserfind_elements_by_css_selector('#kw')[0]
# 6.find_elements_by_link_text
# eg:browserfind_element_by_link_text("新闻")

# 访问元素信息
# 获取元素属性
# .get_attribute('class')
# 获取元素文本
# .text
# 获取标签名
# .tag_name


# 交互
# 点击:click()
# 输入:send_keys()
# 后退操作:browserback()
# 前进操作:browserforword()
# 模拟JS滚动:
# js='document.documentElement.scrollTop=100000'
# browserexecute_script(js) 执行js代码
# 获取网页代码：page_source
# 退出：browserquit()


# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

from selenium import webdriver

import time


path = 'chromedriver.exe'
browser = webdriver.Chrome(path)

url = 'https://www.baidu.com'
browser.get(url)

# 等待2s
time.sleep(2)

# 获取文本框对象
input = browser.find_element_by_id('kw')

# 输入关键字
input.send_keys('bloodborne')

time.sleep(2)

# 获取百度一下搜索按钮对象
search_btn = browser.find_element_by_id('su')

# 点击搜索按钮
search_btn.click()

time.sleep(2)

# 滚动到页面底部（注意：此处写的是js代码）
js_to_page_bottom = 'document.documentElement.scrollTop=100000'
# 执行改js代码
browser.execute_script(js_to_page_bottom)

time.sleep(2)

# 获取下一页按钮
next_btn = browser.find_element_by_xpath('//a[@class="n"]')

# 点击下一页按钮
next_btn.click()

time.sleep(2)

# 回到上一页（后退操作）
browser.back()

time.sleep(2)

# 前进到下一页（前进操作）
browser.forward()

time.sleep(2)

# 关闭浏览器
browser.quit()
