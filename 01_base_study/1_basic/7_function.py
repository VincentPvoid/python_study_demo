# 函数 除了语法和不会进行函数提升之外，其他方面都和js中的函数相同

# python中不会进行函数提升，因此在定义之前调用该函数会报错
# sum(1,2)

def sum(a,b):
  return a + b

print(sum(1,2)) 