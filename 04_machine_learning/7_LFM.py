# LFM梯度下降算法

import numpy as np


# 1. 数据准备
# 评分矩阵R
R = np.array([[4,0,2,0,1],
              [0,2,3,0,0],
              [1,0,2,4,0],
              [5,0,0,3,1],
              [0,0,1,5,1],
              [0,3,2,4,1]])

# print(R.shape[1])


# 2. 算法矩阵
'''
输入参数
R: M * N的评分矩阵
K: 隐特征向量维度
max_iter: 最大迭代次数
alpha: 步长
lamda: 正则化系数

输出
分解之后的P、Q
P: 初始化用户特征矩阵M * K
Q; 初始化物品特征矩阵N * K
'''

# 给定超参数
K = 5
max_iter = 5000
alpha = 0.0002
lamda = 0.004

# 核心算法
def LFM_grad_desc(R, K=2, max_iter=1000, alpha=0.0001, lamda=0.002):
  # 基本维度参数定义
  # 获取原始矩阵的行数
  M = len(R)
  # 获取原始矩阵的列数
  # N = R.shape[1]
  N = len(R[0])

  # 随机生成P、Q初始值
  P = np.random.rand(M, K)
  Q = np.random.rand(N, K)
  # 计算时Q需要转置
  Q = Q.T

  # 开始迭代
  for step in range(max_iter):
    # 对所有的用户u、物品i进行遍历（遍历原始矩阵R），梯度下降计算对应的特征向量Pu、Qi
    for u in range(M):
      for i in range(N):
        # 为0表示没有标记过（无数据），是需要预测的位置
        # 因此需要筛选出不为0的数据，进行误差计算
        if R[u][i] > 0:
          # 使用拆分出来的P、Q中对应的向量相乘，计算预测值（行x列，即P[u, :], Q[:,i]）
          # 预测值 - 当前真实值 = 误差
          # np.dot() 可以计算两个向量相乘
          eui = np.dot(P[u, :], Q[:,i]) - R[u][i]
          # 代入公式，按照梯度下降算法更新当前的Pu、Qi
          # Pu、Qi中需要更新K个值（因为P中每行K个值，Q中每列K个值）
          for k in range(K):
            # 梯度下降迭代公式
            P[u][k] = P[u][k] - alpha * (2 * eui * Q[k][i] + 2 * lamda * P[u][k])
            Q[k][i] = Q[k][i] - alpha * (2 * eui * P[u][k] + 2 * lamda * Q[k][i])
    
    # # u、i遍历完成，所有特征向量更新完成，使用获取到的P、Q计算预测评分矩阵
    # R_pred = np.dot(P, Q)

    # 计算当前损失函数
    cost = 0
    for u in range(M):
      for i in range(N):
        # 有值（不为0）的数据才需要进行损失计算
        if(R[u][i] > 0):
          cost += (R[u][i] - np.dot(P[u, :], Q[:,i]))**2
          # 加上正则化项（根据公式计算）
          # 向量的模长 = 向量中每一项的平方和，开方
          for k in range(K):
            cost += lamda * (P[u][k] **2 + Q[k][i] **2)

    # 如果损失小于某个值，可以结束迭代
    if cost < 0.0001:
      break   
  
  return P, Q.T, cost


P, Q, cost = LFM_grad_desc(R, K, max_iter, alpha, lamda)

# 使用获取到的P、Q计算预测评分矩阵
R_pred = np.dot(P, Q.T)

print(P)
print(Q)
print(R_pred)
print(cost)
          


