# 字典高级

p1 = {'name':'Maria', 'age':18}

print(p1['name'])
print(p1['age'])
# 如果使用不存在的key则会报错；注意这点与js不同
# print(p1['work']) 

# 注意；python中无法使用obj.xxx方法来获取对应key的值

# 使用get方法获取数据，可以使用不存在的key，会返回None，不会报错
print(p1.get('name'))
print(p1.get('work')) # None
temp = p1.get('work')
print(type(temp)) # <class 'NoneType'>



# 删除字典中的元素
# del 删除指定的元素 或删除字典本身
# clear() 清空字典，不删除字典本身

# del 删除指定的元素 或删除字典本身；与js中delete用法相同
p2 = {'name':'plain doll', 'age': 20}
# del 删除指定的元素 
print(p2)
# del p2['age']
# print(p2) # {'name': 'plain doll'}

# del 删除字典本身
# del p2
# print(p2) # 报错

# clear() 清空字典，不删除字典本身，保留字典对象；js中一般使用obj={}来重置
p2.clear()
print(p2) #{}




# 字典的遍历
# 遍历字典的key；与js中Object.keys()类似，但语法不同
keys = p1.keys()
print('keys ',keys) # dict_keys(['name', 'age'])


# 遍历字典的value；与js中Object.values()类似，但语法不同
values = p1.values()
print('values ',values) # dict_values(['Maria', 18])


# 遍历字典的项（元素）；js中无对应方法
items = p1.items()
print('items ', items) # dict_items([('name', 'Maria'), ('age', 18)])

# 返回的每个项的数据格式类似于元组[('name', 'Maria'), ('age', 18)]
for item in items:
  print(item)

# 遍历字典的key-value（键值对）
for key,value in items:
  print('key ', key)
  print('value ', value)

# 使用dict.items()得到字典项，使用for循环遍历所有字典项时
# 如果只使用一个参数，返回的每个字典项的数据格式为(key, value)；
# 使用两个参数时，分别返回key和value