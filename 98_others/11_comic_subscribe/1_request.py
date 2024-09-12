import requests
from bs4 import BeautifulSoup

# 测试保存html用
def saveHtml(file_name, file_content):
  # 注意windows文件命名的禁用符，比如 /
  with open(file_name.replace('/', '_') + ".html", "w", encoding='utf-8') as f:
    f.write(file_content)


# 获取订阅页html文件
def getTargetContent():
  url = 'https://i.idmzj.com/ajax/my/subscribe'
  headers = {
    'Cookie':  'your cookie'
  }
  data = {
    "page": 1,
    "type_id": 1,
    "letter_id": 0,
    "read_id": 1,
  }
  response = requests.post(url=url, data=data, headers=headers)
  content = response.text
  # saveHtml('test', content)
  return content


# 获取对应名称并保存到文件中
def saveTitleList(content, file_name='comic_titles'):
  soup = BeautifulSoup(content, 'lxml')
  title_a_list = soup.select('.dy_content_li .dy_r h3 a')
  # print(title_list)
  with open(f'./{file_name}.txt', mode='w', encoding='utf-8') as fp:
    text = ''
    for i in range(len(title_a_list)):
      title = title_a_list[i].text
      # print(title)
      text += title + '\n'
    text += f'\n共{i+1}条'
    fp.write(text)
  


def main():
  content = getTargetContent()
  saveTitleList(content)


if __name__ == '__main__':
  main()
