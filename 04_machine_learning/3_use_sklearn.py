# 使用sklearn实现线性回归

import numpy as np
import matplotlib.pyplot as plt

# 1.导入csv文件数据
points = np.genfromtxt('./data.csv', delimiter=',')

# 提取points中的两列数据，分别作为x，y
x = points[:, 0]
y = points[:, 1]

# 2.定义损失函数
def compute_cost(w, b, points):
  total_cost = 0
  M = len(points)

  for i in range(M):
    x = points[i, 0]
    y = points[i, 1]
    total_cost += (y - w * x - b) ** 2
  
  return total_cost / M


# 使用sklearn中的线性回归方法
from sklearn.linear_model import LinearRegression
lr = LinearRegression()

# 使用库中自带的方法进行拟合
# 注意参数应该是二维的嵌套数组，否则会报错
# lr.fit(x,y) # 报错

# 使用reshape方法改变数组或矩阵的形状
# a.reshape(m,n)表示将原有数组a转化为一个m行n列的新数组，a自身不变；m与n的乘积等于数组中的元素总数
# 参数m或n其中一个可写为-1，当为-1时，会根据原数组中的元素总数自动计算行或列的值
# 下面表示转换为行数不限，列数为1的嵌套数组
x_new = x.reshape(-1, 1)
y_new = y.reshape(-1, 1)

# print(x_new)

# 拟合
lr.fit(x_new, y_new)

# 从训练好的模型中提取系数和截距；
# 注意返回的数据结构（w为嵌套数组，b为数组），
# w = lr.coef_   # [[1.32243102]]
# b = lr.intercept_  # [7.99102098]

# 如果需要使用w, b，还需要获取对应值
w = lr.coef_[0][0]
b = lr.intercept_[0]

print('w is: ', w) 
print('b is: ', b)

cost = compute_cost(w, b, points)
print('cost is: ', cost)


# 画出拟合曲线
plt.scatter(x, y)
pred_y = w * x + b

plt.plot(x, pred_y, c='r')
plt.show()

