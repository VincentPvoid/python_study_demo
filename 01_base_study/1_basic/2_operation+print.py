# 在python中，+加号两端都是字符串才可以进行加法运算；如果一端为int整型，则会报错
# a = 123
# b = '456'
# print(a + b)


# 在python中，字符串进行乘法运算，是加字符串重复n次
# a = 'test '
# print(a * 3)

# 连续赋值
# a = b = 1
# print(a,b)

# 多个变量赋值；与其他语言不同，其他语言一般不支持这种赋值方法
# a,b,c = 1,2,3
# print(a,b,c)


# 逻辑运算符
# 与and 或or 非not 注意写法与其他语言不同；其他都相同



# 普通输出
# print('test1')

# # 格式化输出
# username = 'Maria'
# age = 18

# # %s 代表字符串 %d 代表数值
# print('my name is %s, I am %d years old' % (username, age))


# 输入
# username = input('please input your name')
# print('My name is : %s' % username)



# if...else语句 功能相同；注意语法格式与js不同；包含条件的括号可以省略不写
# a = 2
# if(a==1): 
#   print('true')
# else: 
#   print('false')



# 练习1
# age = int(input('please input your age '))
# # print(type(age))
# # 注意python中str和int不能进行比较，会报错
# if (age > 18):
#   print('OK')
# else:
#   print('NO')


# 练习2
# 注意else if的写法，python中是简写为elif
# age = int(input('please input your age '))
# if(age > 50):
#   print('Old')
# elif(age > 30):
#   print('Middle')
# elif(age > 18):
#   print('Teen')
# else:
#   print('young')



# for循环
# 循环遍历字符串
# str = 'test1'
# for key in str:
#   print(key)


# range循环
# 如果只有一个参数，则为range(结束值)；遍历区间为左闭右开区间；例子中表示遍历0-4；
# for i in range(5):
#   print(i)

# 如果有两个参数，表示range(起始值，结束值)；遍历区间为左闭右开区间；例子中表示遍历1-5；
# for i in range(1,6):
#   print(i)

# 如果有三个个参数，表示range(起始值，结束值，步长)；遍历区间为左闭右开区间；例子中表示的循环为for(let i = 1;i<10;i+3)；
# for i in range(1,10,3):
#   print(i)


# 循环遍历列表
names_list = ['Maria', 'plain doll', 'Ellee', 'Gerham','hunter']

# 遍历列表中的元素
# for item in names_list:
#   print(item)

# 遍历列表的下标；len方法可以获取列表长度
for i in range(len(names_list)):
  print(i)