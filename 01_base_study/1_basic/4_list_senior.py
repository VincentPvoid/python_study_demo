# 列表高级

# append会把新元素添加到列表末尾
# insert(index, object) 在指定位置index前插入元素object
# 通过extend可以将另一个列表中的元素逐一添加到列表中


# append 把一个新元素插入到列表末尾；与js中数组的push()类似，但只能传一个参数，多了会报错
list1 = [1,2,3,4,5]
list1.append(6)
print('list1 ',list1)

# insert(index, object) 在指定下标插入新元素；js中可用splice(index,0,obj)实现
list2 = ['a','c','d']
list2.insert(1,'b')
print('list2 ', list2)

# extend 连接两个列表，把后面参数中的列表连接到前面的列表中；
# 与js中数组的concat()类似（但concat不改变原数组而是生成新数组，参数也可以传单个元素不一定是数组），而只能连接两个列表（只能传一个参数）
list3 = [11,22]
list4 = [33,44,55]
list3.extend(list4)
# list3.extend(3) # 只能传一个参数，而且必须是列表，如果不满足则报错
print('list3 ',list3)


# 查找和修改元素；与js中数组相同，可以根据下标获取指定元素和修改
list5 = [1,2,3]
print(list5[2]) # 3


# in和 not in；js中可以使用includes返回的值进行判断
# in元素是否存在于该数组，存在时返回True
list6 = [1,2,3,4,5]
print(3 in list6) # True
print(33 in list6) # False

# not in元素是否不存在于该数组，不存在时返回True
# print(33 not in list6) # True
# print(3 not in list6) # False


# 删除列表中的元素
# del：根据下标进行删除
# pop：删除最后一个元素
# remove：根据元素的值进行删除

# del：根据下标进行删除；如果没有该下标（下标超出范围）会报错；
# js中可以使用splice(i,1[,0])达到同样的效果；但不同的是使用splice中没有该下标时不会报错，会返回空数组，而python中del操作没有返回值
list7 = [1,2,3,4,5]
del list7[1] # 不能超出列表的下标；该操作没有返回值，无法接收
print('list7 ',list7) # [1, 3, 4, 5]

# pop：删除最后一个元素；
# 与js中数组的pop()类似，返回值都为被删除的最后一个元素；但js中可以pop空数组（返回undefined），pytho中不能pop空数组（会报错）；
list8 = [1,2,3,4,5]
# a = list8.pop()
print('list8 ', list8) # [1, 2, 3, 4]

# remove：根据元素的值进行删除，该操作返回值为被删除的元素；如果当前列表中没有指定的值则会报错
# js中需要先找到目标元素的下标再进行删除 indexOf()然后splice()
list9 = [11,22, 33, 44, 55]
temp = list9.remove(223)
print('list9 ', list9) # [11, 33, 44, 55]


