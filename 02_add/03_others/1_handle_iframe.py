from selenium import webdriver
# 引入动作链对应的类
from selenium.webdriver import ActionChains
import time

path = 'chromedriver.exe'
browser = webdriver.Chrome(path)

url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)

# 以下操作无法获取目标元素，因为该目标元素位于iframe中
# div = browser.find_element('id' ,'draggable')

# 如果定位的标签存在于iframe中，则必须使用以下方法进行标签定位
browser.switch_to.frame('iframeResult') # 切换浏览器标签定位的作用域
div = browser.find_element('id' ,'draggable')

# 动作链
action = ActionChains(browser)
# 点击长按指定的元素
action.click_and_hold(div)

for i in range(5):
  # perform()立即执行动作链操作
  # move_by_offset(x, y) x水平方向，y垂直方向
  action.move_by_offset(25,0).perform()
  time.sleep(0.5)

# 释放动作链
action.release()

# 关闭浏览器
browser.quit()


# print(div)
