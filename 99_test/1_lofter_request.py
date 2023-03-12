import requests
import re
import random

url = 'https://www.lofter.com/dwr/call/plaincall/PostBean.getPosts.dwr'

headers={
  "Content-Type":"text/plain",
  "referer": 'https://www.lofter.com',
  # "origin": "https://www.lofter.com",
  "cookie": "your own cookie",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
  # "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
  # "sec-ch-ua-mobile": "?0",
  # "sec-ch-ua-platform": "Windows",
  # "sec-fetch-dest": "empty",
  # "sec-fetch-mode": "cors",
  # "sec-fetch-site": "same-origin",
}
startNum = 0

# contentReg = re.compile('\.content="(.*?)";')

def get_content(currentNum):
  randomNum = random.randint(100000, 999999)
  data = {
    'callCount': 1,
    'scriptSessionId': '${scriptSessionId}187',
    'httpSessionId':'',
    'c0-scriptName' : 'PostBean',
    'c0-methodName' : 'getPosts',
    'c0-id' : 0,
    'c0-param0': 'number:xxxxxx', # 根据这个确定要请求的是哪个blog的数据
    # 'c0-param1': 'number:20', # 每页条目数量
    # 'c0-param2': 'number:0', # 当前条目位置（0表示最初）
    'c0-param1': 'number:100', # 每页条目数量（最多100?）
    'c0-param2': 'number:' + str(currentNum), # 当前条目位置（0表示最初）
    'batchId' : randomNum # 6位随机数
  }
  print(data)
  response = requests.post(url=url, data=data, headers=headers)
  # contentStr = response.text
  content = response.text
  # content = contentReg.search(contentStr).group()
  # content = re.findall(contentReg, contentStr)
  # print(content)
  # startNum = currentNum + 100
  return content

def save_ori_text(index, content):
  with open('./daily_ori_page' + str(index) + '.txt', 'w', encoding='utf-8') as fp:
    fp.write(content)

# get_content(0)
# print(startNum, 'bbbbbbbbbb')


if __name__ == '__main__':
  for i in range(4):
    # print(i)
    startNum = i * 100
    content = get_content(startNum)
    save_ori_text(i, content)


# 需要的字符串字段
# content="xxxxxx" 内容
# createTime=xxxxxx 发表时间
# tag="xxx,xx" 标签，如果有多个，其中用,分割

# 当该值后面的数组为空时表示已经到了第一篇文章，没有更多可加载
# dwr.engine._remoteHandleCallback('124312','0',[s2,s3,s4,s5]); 


