# 简单线性回归（最小二乘法）

import numpy as np
import matplotlib.pyplot as plt

# 1.导入csv文件数据；delimiter表示分割符
points = np.genfromtxt('./data.csv', delimiter=',')

# print(points)

# 提取points中的两列数据，分别作为x，y
x = points[:, 0]
y = points[:, 1]

# print(x,y)

# 用plt画出散点图
# plt.scatter(x, y)
# plt.show()


# 2.定义损失函数
# 损失函数是系数的函数，还需要另外传入数据的x，y
def compute_cost(w, b, points):
  total_cost = 0
  M = len(points)

  # 逐点计算平方损失误差，然后求平均数
  for i in range(M):
    x = points[i, 0]
    y = points[i, 1]
    total_cost += (y - w * x - b)**2

  return total_cost / M


# 3.定义算法拟合函数（最终得到形式为 y= wx + b 这样的直线）
# 先定义一个求均值的函数
def average(data_list):
  sum = 0
  length = len(data_list)
  for i in range(length):
    sum += data_list[i]
  return sum / length

# 定义核心拟合函数
def fit(points):
  M = len(points)
  x_bar = average(points[:, 0])

  sum_yx = 0
  sum_x2 = 0
  sum_delta = 0
  # temp = 0

  # 根据公式计算w；
  # 其中w公式右下方的值可以用x_bar进行计算，简化算法
  for i in range(M):
    x = points[i, 0]
    y = points[i, 1]
    sum_yx += y * (x - x_bar)
    sum_x2 += x ** 2
    # temp += x

  # 使用x计算，比较麻烦
  # temp = temp ** 2 / M
  # w = sum_yx / ( sum_x2 - temp ) 
  # print(w)

  # 使用x_bar计算，较为简洁
  w = sum_yx / (sum_x2 - M * (x_bar**2))
  # print(w)

  for i in range(M):
    x = points[i, 0]
    y = points[i, 1]
    sum_delta += y - w * x

  b = sum_delta / M  

  return w, b

# 4.测试
w, b = fit(points)
cost = compute_cost(w, b, points)
print('w is: ', w) # 1.3224310227553846
print('b is: ', b) # 7.991020982269173
print('cost is: ', cost) # 110.25738346621313


# 5.画出拟合曲线
plt.scatter(x, y)
# 针对每一个x，计算出预测的y值
pred_y = w * x + b
# c='r'表示颜色为红色
plt.plot(x, pred_y, c='r')
plt.show()


