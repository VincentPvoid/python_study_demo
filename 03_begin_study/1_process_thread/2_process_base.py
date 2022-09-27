# 多进程


from multiprocessing import Process
import time
import random

def info(name):
    print(f"Process-{name} info stats....")
    time.sleep(random.randrange(1,7))
    print(f"Process-{name} info ends....")

if __name__ == "__main__":
  	# args参数传给target指向的
    p1 = Process(target=info,args=("p1",))
    p2 = Process(target=info,args=("p2",))
    p3 = Process(target=info,args=("p3",))

    p1.start()
    p2.start()
    p3.start()
    print("main")