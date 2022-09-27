# 在python，使用open函数，可以打开一个已经存在的文件，或者创建一个新文件
# open(文件路径，访问模式) 如果只写文件路径则访问模式默认为r，当该文件不存在时报错
# 访问模式：w 可写 r可读
# 该方法可以打开已存在的文件或创建一个新文件（为r模式时不能创建）；但不能创建新文件夹，暂时需要手动创建

# fp = open('./file_demo/test1.txt', 'w')

# 当该文件存在时不报错；不存在时报错
# fp = open('./file_demo/test1.txt')

# fp1 = open('./file_demo/test1.txt', 'w')

# 如果该文件不存在，则为创建新文件并写入数据；如果该文件存在，原内容会被新数据替代
# 注意在该例子中，文件并不在同级目录下，因此如果目标文件所在的文件夹不存在，会报错，不会进行创建
# fp1.write('test1\n'*5)

# 打开文件后应该进行关闭
# fp1.close()



# 对文件进行追加而不是替代
fp2 = open('./file_demo/test2.txt', 'a')
fp2.write('test2\n')
# fp2.close()

# 读取文件数据(read)
# 使用read(num)可以从文件中读取数据，num表示要从文件中读取的数据的长度（单位是字节），如果没有传入num，那么就表示读取文件中所有的数据
# 读取文件时需要用读方法打开
# fp2r = open('./file_demo/test2.txt', 'r')

# 默认情况下，read为一字节一字节地读取数据，效率较低，速度较慢
# fp2Content = fp2r.read()

# fp2Content = fp2r.read(3) 
# print(fp2Content) # tes
# print("‐"*30) # 分割线，用来测试
# fp2Content = fp2r.read() # 从上次读取的位置继续读取剩下的所有的数据

# readline()为一行读取，但只能读取一行
# fp2Content = fp2r.readline()
# print(fp2Content)


# readlines可以按照行的方式把整个文件中的内容进行一次性读取，并且返回的是一个列表，其中每一行为列表的一个元素
# fp2Content = fp2r.readlines()

# print(fp2Content)

# fp2r.close()



# 文件的序列化和反序列化
# 序列化：把不是字符串格式的数据转换为JSON字符串；使用json.dump()或json.dumps()；用法类似用js中的JSON.stringify
# 反序列化：把字符串格式JSON字符串转换为python对象；使用json.load()或json.loads()；用法类似用js中的JSON.parse
# 注意在python中json是小写
# 非字符串格式的数据无法直接写入文件中，因此需要进行序列化的转换

# fp3 = open('./file_demo/test3.txt','w')

# hunters_list = ['Maria', 'plain doll', 'Ellen', 'Vrtra']
# # # 报错，不能直接写入列表
# # # fp3.write(hunters_list) # TypeError: write() argument must be str, not list

# # # 使用JSON进行序列化时需要先引入
# import json
# # # 使用json.dumps()进行序列化
# huntersStr = json.dumps(hunters_list)
# # # 写入文件中
# fp3.write(huntersStr)

# print(type(hunters_list)) # list
# print(type(huntersStr)) # str

# fp3.close()


# 使用json.dump()；相当于简化操作，转换和写入同时进行
# fp4 = open('./file_demo/test4.txt','w')
# test_list = ['a','b','c']
# import json
# json.dump(test_list, fp4)

# fp4.close()



# 反序列化

# 使用json.loads()进行反序列化
fp3 = open('./file_demo/test3.txt','r')
# print(type(fp3)) # <class '_io.TextIOWrapper'>
import json

fp3Content = fp3.read()
print(fp3Content, type(fp3Content)) # ["Maria", "plain doll", "Ellen", "Vrtra"] <class 'str'>
# 反序列化
fp3Content = json.loads(fp3Content)
print(type(fp3Content)) # <class 'list'>
fp3.close()

print('===========================')

# 使用json.load()；相当于简化操作，读取文件和转换同时进行
fp4 = open('./file_demo/test4.txt','r')
res = json.load(fp4)
print(res, type(res)) # ['a', 'b', 'c'] <class 'list'>
fp4.close()