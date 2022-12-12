# 简单线性回归（梯度下降法）

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


# 3. 定义模型的超参数
# 梯度下降步长
alpha = 0.0001
# w的初始值
init_w = 0
# b的初始值
init_b = 0
# 迭代次数
num_iter = 10


# 4. 定义核心梯度下降算法函数
def grad_desc(points, init_w, init_b, num_iter):
  w = init_w
  b = init_b

  # 定义一个list保存所有的损失函数值，用来显示下降的过程
  cost_list = []

  for i in range(num_iter):
    # 把每次算出的损失函数放入list中
    cost_list.append(compute_cost(w, b, points))
    w, b = step_grad_desc(w, b, alpha, points)
  
  return [w, b, cost_list] 



# 迭代更新w和b的算法
def step_grad_desc(current_w, current_b, alpha, points):
  sum_grad_w = 0
  sum_grad_b = 0
  M = len(points)

  # 对每个点，代入公式求和
  for i in range(M):
    x = points[i, 0]
    y = points[i, 1]
    sum_grad_w += ( current_w * x + current_b - y ) * x
    sum_grad_b += current_w * x + current_b - y
  
  # 用公式求当前梯度
  grad_w = 2 / M * sum_grad_w
  grad_b = 2 / M * sum_grad_b
  
  # 梯度下降，更新当前的w和b
  new_w = current_w - alpha * grad_w
  new_b = current_b - alpha * grad_b

  return new_w, new_b


# 5 测试：运行梯度下降算法计算最优的w和b
w, b, cost_list = grad_desc(points, init_w, init_b, num_iter)
print('w is: ', w)
print('b is: ', b)

cost = compute_cost(w, b, points)
print(cost)

# 传入参数为list时，会以list的下标为x，值为y进行作图
plt.plot(cost_list)
plt.show()


# 6. 画出拟合曲线
plt.scatter(x, y)
pred_y = w * x + b

plt.plot(x, pred_y, c='r')
plt.show()

