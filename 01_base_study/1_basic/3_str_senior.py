# 字符串高级

# 获取长度:len len函数可以获取字符串的长度。
# 查找内容:find 查找指定内容在字符串中是否存在，如果存在就返回该内容在字符串中第一次出现的开始位置索引值，如果不存在，则返回-1.
# 判断:startswith,endswith 判断字符串是不是以谁谁谁开头/结尾
# 计算出现次数:count 返回 str在start和end之间 在 mystr里面出现的次数
# 替换内容:replace 替换字符串中指定的内容，如果指定次数count，则替换不会超过count次。
# 切割字符串:split 通过参数的内容切割字符串
# 修改大小写:upper,lower 将字符串中的大小写互换
# 空格处理:strip 去空格
# 字符串拼接:join 字符串拼接


str1 = 'test'

# len 获取长度；相当于str.length，注意用法的不同
# print(len(str1)) # 4

# find；相当于str.indexOf，用法也相似；当有第二个参数时表示从该下标开始查找目标值
# print(str1.find('t')) # 0
# print(str1.find('t',2)) # 3

# startswith 判断字符串是不是以xxx开头，返回值为Boolean；其实可以使用find返回的下标进行判断
# print(str1.startswith('te')) # True
# print(str1.startswith('e')) # False

# # endswith 判断字符串是不是以xxx结尾，返回值为Boolean；其实可以使用find返回的下标进行判断
# print(str1.endswith('te')) # False
# print(str1.endswith('t')) # True

# count 返回str在start和end之间，指定值在范围内出现的次数；格式：str.count(指定值，[起始下标，结束下标])，不包括结束下标
str2 = 'testaaat'
# print(str2.count('t')) # 3
# print(str2.count('t',0, 7)) # 2

# replace 
# 与js中str.replaceAll类似，但必须至少指定2个参数，也可以指定替换的次数（如果不设定则默认替换全部），从头开始替换
# 格式 str.replace(被替换值，新值，[最多替换次数])
# print(str2.replace('t','b')) # besbaaab
# print(str2.replace('t','b',2)) # besbaaat


# slipt 与js中str.split类似，但不能使用''空串进行分割
# print(str1.split('')) # 报错
# print(str1.split('e')) # ['t','st']


# upper把字符串变为小写；lower把字符串变为大写；
# 与js中toUpperCase和toLowerCase相同
str3 = 'AbCdef'
# print(str3.upper()) # ABCDEF
# print(str3.lower()) # abcdef


# strip 与js中trim相同，去除字符串头尾空格
str4 = '  space  '
str5 = ' space test  '
print(str4.strip())
print(str5.strip())


# join 字符串拼接；把该字符串插入到目标字符串头尾之间；用法非常诡异，所以一般不用
str6 = 'a'
print(str6.join('bbb')) # babab