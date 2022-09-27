# 多线程

# 线程类
from threading import Thread

# # 直接使用Thread写法
# def func():
#   for i in range(500):
#     print('func' , i)

# if __name__ == '__main__':
#   # 创建线程并给线程安排任务
#   t = Thread(target=func)
#   # 执行start()方法，表示该多线程状态为可以开始工作状态；
#   # 注意并不表示马上开始执行，实际执行时间还是由CPU决定
#   t.start()
#   for i in range(500):
#     print('main', i)

# # 继承Thread写法
# class CusThread(Thread):
#   def run(self):
#     for i in range(500):
#       print('sub thread', i)

# if __name__ == '__main__':
#   t = CusThread()
#   # 执行start()方法，其实就是调用Thread类中的run()方法；
#   # t是CusThread生成的实例，调用run时会使用CusThread中重写的run()；类似于js中的类和原型链继承
#   t.start()
#   for i in range(500):
#     print('main thread', i)

# 直接使用Thread写法；多个进程可以使用参数进行区分
# def func(t_name):
#   for i in range(500):
#     print(t_name , i)

# if __name__ == '__main__':
#   # 注意传递自定义参数的名称，而且必须以元组的形式传递
#   # 注意要加逗号，否则不会识别为元组类型
#   t1 = Thread(target=func, args=('t1',) )
#   t1.start()
#   t2 = Thread(target=func, args=('t2',) )
#   t2.start()


# 继承Thread写法；加入参数
class CusThread(Thread):
  def __init__(self, name):
    # 必须super()方法先，不然会覆盖__name
    super(CusThread, self).__init__()
    self.__name = name

  def run(self):
    for i in range(500):
      print(self.__name, i)


if __name__ == '__main__':
  t1 = CusThread('t1')
  t1.start()
  t2 = CusThread('t2')
  t2.start()

# 非多线程；按顺序执行
# def func():
#   for i in range(500):
#     print('func' , i)

# if __name__ == '__main__':
#   func()
#   for i in range(500):
#     print('main', i)