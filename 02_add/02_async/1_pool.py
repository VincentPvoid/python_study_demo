# 线程池基本使用案例

import time

# 模拟使用单线程串行方式执行
# def get_page(str):
#   print('start ', str)
#   time.sleep(2)
#   print('finish ', str)

# test_list = ['aa', 'bb', 'cc', 'dd']
# start_time = time.time()

# for i in range(len(test_list)):
#   get_page(test_list[i])

# end_time = time.time()
# print('%d second' % (end_time - start_time))


# 导入线程池模块对应的类
from multiprocessing.dummy import Pool
# 使用线程池方式执行
start_time = time.time()
def get_page(str):
  print('start ', str)
  time.sleep(2)
  print('finish ', str)

test_list = ['aa', 'bb', 'cc', 'dd']

# 实例化一个线程池对象
pool = Pool(4)

pool.map(get_page, test_list)

end_time = time.time()
print('%d second' % (end_time - start_time))
