# import sys
# sys.path.append("D:\Python\Python310\Lib\site-packages")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# 注意--的问题，如果输入错误则无法实现无界面
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu') 
# chrome_options.add_argument("--no-sandbox")
path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.binary_location = path
browser = webdriver.Chrome(chrome_options=chrome_options)


browser.get('https://www.baidu.com/')

browser.save_screenshot('baidu.png')


# 封装无界面浏览器函数
def share_browser():
  # 初始化
  chrome_options = Options()
  # 注意--的问题，如果输入错误则无法实现无界面
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-gpu') 
  # chrome_options.add_argument("--no-sandbox")
  # chrome路径
  path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
  chrome_options.binary_location = path
  browser = webdriver.Chrome(chrome_options=chrome_options)
  return browser


# 封装调用
# from handless import share_browser
# browser = share_browser()
# browser.get('http://www.baidu.com/')
# browser.save_screenshot('handless1.png')