from urllib import response
import requests
from bs4 import BeautifulSoup

# 该案例其实用不上年份参数，但是为了还原所以写一下
def get_data_csv(year):
  # url = 'http://www.piaofang.biz/' + year

  url = 'http://www.piaofang.biz/'

  response = requests.get(url=url)

  # 指定响应数据编码，否则会乱码
  response.encoding = 'gb2312'
  content = response.text

  # print(response.encoding)
  # print(content)

  # 第二个参数表示使用html解析器
  soup = BeautifulSoup(content, 'html.parser')

  fp = open('movie_box_offset.csv', mode="a",encoding='utf-8')

  tr_list = soup.find_all('tr')
  # print(tr_list,'bbbbbbbb')
  for tr in tr_list:
    # print(type(tr))
    # print(tr.get('class'))
    # 去掉第一行表格标题（其实可以用，但为了之后方便还原案例所以先去掉）
    trClass = tr.get('class')
    if(trClass and trClass[0] == 'fenlei'):
      # print('bbbbbbbbbbbbbbb')
      continue
    
    # 获取该行所有td
    td_list = tr.find_all('td')
    # 如果该行不为空（有td）
    if(len(td_list) != 0):
      for td in td_list:
        # print(td.get_text())
        
        # 获取td中的文本并去除空格
        # strip()默认去掉两端的空白（空格、换行符、制表符）类似js中的trim()；这里没有换行其实不需要使用，但还是顺便记录一下
        td_content = td.get_text().strip()
        # 如果文本中含有, 需要在文本两边加上双引号，否则csv文件进行数据处理时可能会有问题
        if(td_content.find(',')!= -1):
          td_content = '"'+td_content+'"'
        
        fp.write(td_content)
        # fp.write(td.get_text().strip())
        fp.write(',')
      fp.write('\n') # 加入换行符

  fp.close()


# 该案例其实并不需要循环，但是为了还原所以写一下
# for year in range(2008, 2019):
#   get_data_csv(year)

get_data_csv(1)

