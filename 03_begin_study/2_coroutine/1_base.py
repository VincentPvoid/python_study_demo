# 协程概念

import time

def func():
  print(1)
  time.sleep(3)  # 当前的线程处于阻塞状态
  print(2)



# 使用input()时，程序也是处于阻塞状态
# requests.get() 在网络请求返回数据之前，程序也处于阻塞状态
# 一般情况下，程序处于IO操作时，线程都会处于阻塞状态


# 协程：
# 在单线程条件下
# 当程序处于IO操作时，可以选择性地切换到其他任务上
# 在微观上，是一个一个任务进行切换，一般切换条件为遇到IO操作
# 在宏观上，用户看到的其实是多个任务在一起执行