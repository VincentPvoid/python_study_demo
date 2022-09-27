# 线程池：一次性开辟一些线程，用户直接像线程池提交任务，由线程池进行线程任务的调度

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def fn(name):
  for i in range(500):
    print(name, i)

if __name__ == "__main__":
  # 创建线程池
  with ThreadPoolExecutor(50) as t:
    for i in range(100):
      t.submit(fn, name=f"thread{i}")
  print('finish')

# 进程池的用法与上面相似，把ThreadPoolExecutor替换为ProcessPoolExecutor即可
