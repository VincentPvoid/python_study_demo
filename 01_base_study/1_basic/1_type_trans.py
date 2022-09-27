# 爬虫时大部分获取的都是字符串类型

# 转换为整型int
# a = '123'
# print(type(a))
# # 将字符串转换为整数
# b = int(a)
# print(type(b)) # int


# float转换为int
# a = 1.23
# print(type(a))
# # 如果将float转为整数int，只会保留整数部分
# b = int(a)
# print(b) # 1


# boolean转换为int
# a = True
# print(int(a)) # 1
# b = False
# print(int(b)) # 0


# 以下两种情况将会转换失败
# 123.456和12ab字符串，都包含非法字符，不能被转换为整数，会报错
# 如果字符串中包含非法字符串，则报错
# print(int('123.456'))
# print(int('12ab'))








# 爬虫时大部分时候获取的都是字符串类型

# 将str字符串类型转换为float浮点数类型
# a = '1.23'
# print(type(a)) # <class 'str'>
# b = float(a)
# print(b) #1.23
# print(type(b)) # <class 'float'>


# 将int转换为float
# a = 123
# print(type(a)) # <class 'int'>
# b = float(a)
# print(b) # 123.0
# print(type(b)) # <class 'float'>



# 整型转换为字符串 大部分的应用场景
# a = 123
# b = str(a)
# print(b)
# print(type(b)) # <class 'str'>

# boolean转换为字符串
# a = True
# b = str(a)
# print(b)
# print(type(b))



# 其他类型转换为boolean

# list
# a = [1,2,3]
# b = []
# print(bool(a))
# print(bool(b)) # False

# # tuple
# c = ('a',1,3)
# d = ()
# print(bool(c))
# print(bool(d)) # False

# dist字典
# a = {'name':'test', 'age':12}
# b = {}
# print(bool(a))
# print(bool(b)) # False

# 为False的情况
#  0（包括float浮点类型的0.0）
# 空串
# 没有数据的list（即[]；注意这点与js中数组的不同）
# 没有数据的tuple元祖（即()）
# 没有数据的dist字典（即{}；注意这点与js中对象的不同）
print(bool(0))
print(bool(0.0))
print(bool(''))
print(bool([]))
print(bool(()))
print(bool({}))
print(bool(False))