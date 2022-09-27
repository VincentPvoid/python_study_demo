# 读取文件异常
# 在读取一个文件时，如果这个文件不存在，则会报出 FileNotFoundError 错误

# fp = open('test.txt', 'r')

try:
  fp = open('./file_demo/test.txt', 'r')
  fp.read()
  fp.close()
except FileNotFoundError:
  print('not found file')
