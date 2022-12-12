# k means教程

import numpy as np
import matplotlib.pyplot as plt

# 从sklearn中生成聚类数据
from  sklearn.datasets._samples_generator import make_blobs


# 1 数据加载
# n_features表示每一个样本有多少特征值；简单说就是样本点的数组中有几个数据；默认为2
# n_samples表示样本的个数
# centers是聚类中心点的个数，可以理解为label的种类数
# random_state是随机种子，可以固定生成的数据
# cluster_std设置每个类别的方差
# 生成的x为格式为[[],[],[]...]二维嵌套数组形式的数据
# 生成的y为类别一维数组；在该例子中不需要使用
x, y = make_blobs(n_samples=100, centers=6, random_state=1234, cluster_std=0.6)

# print(x)

# 设置画出的图的大小
plt.figure(figsize=(6,6))
plt.scatter(x[:,0], x[:,1], c=y)
plt.show()


# 2 算法实现
# 引入scipy中的距离函数，该函数默认计算欧式距离
from scipy.spatial.distance import cdist

# k-means实现
class K_Means(object):
  # n_clusters(K)类别；max_iter迭代次数、centroids初始质心
  def __init__(self, n_clusters=6, max_iter=300, centroids=[]):
    self.n_clusters = n_clusters
    self.max_iter = max_iter
    # 把质心转换为数组类型，数据为float浮点型（如果直接输入[[]]，会是list类型，不能使用shape等属性）
    self.centroids = np.array(centroids, dtype=np.float64)

  # 训练模型方法，k-means聚类过程，传入原始数据
  def fit(self, data):
    # 如果没有指定初始质心，则随机选取data中的点作为初始质心；如果self.centroids没值，则对应的shape值为(0,)
    if(self.centroids.shape == (0,)):
      # np.random.randint(最小值，最大值，数量) 随机生成在范围内指定数量的整数
      self.centroids = data[np.random.randint(0, data.shape[0], self.n_clusters)]
    
    # 进行迭代
    for i in range(self.max_iter):
      # 1 计算距离矩阵；scipy中的距离函数要求参数为同维度，即可进行计算
      # 结果为(100,6)的矩阵；每一行的6个数据分别为距离6个质心点的距离
      distance = cdist(data, self.centroids)

      # 2 把距离从近到远排序，选取距离最近的质心点的类别，作为当前点的分类
      # np.argmin() 返回值最小的数据对应的下标值（因为该例子中类别就是和下标相同的数字，因此结果中的值其实就是类别）
      # 结果为100*6的矩阵[x x x x x ...]
      c_index = np.argmin(distance, axis=1)

      # 3 对每一类数据进行均值计算，更新质心点坐标
      for i in range(self.n_clusters):
        # 如果该类别在c_index中存在
        if i in c_index:
          # 选出所有类别是i的点，取data里坐标的均值，更新第i个质心
          # np.mean() 求数组平均值；此处axis为0表示把对应每一行的数值相加，再取平均值
          # python中数组可以直接与数字进行比较
          # 数组的布尔下标类型，类似于js中Array.filter()的效果，在生成的新数组中保留原数组中对应位置为True的值
          self.centroids[i] = np.mean(data[c_index == i], axis=0)

  # 实现预测方法
  def predict(self, samples):
    # 跟上面一样，先计算距离矩阵，然后选取距离最近的质心的类别
    distance = cdist(samples, self.centroids)
    c_index = np.argmin(distance, axis=1)
    return c_index



# 3.测试
# 定义绘制子图的函数
# x,y 绘图所需坐标；centeroids质心点（形式与x相同，都为每行有2个数据的嵌套数组）；subpolt子图编号；title子图名称
def plotKMeans(x, y, centeroids, subpolt, title):
  # 分配子图
  plt.subplot(subpolt)
  # 画图
  plt.scatter(x[:, 0], x[:, 1], c='r')
  # 画出质心点；s设置点的大小
  plt.scatter(centeroids[:, 0], centeroids[:, 1], c=np.array(range(6)), s=100)
  plt.title(title)



kmeans = K_Means(max_iter=300, centroids=np.array([[3,1],[3,2],[3,3],[3,4],[3,5],[3,6]]))

plt.figure(figsize=(10,6))

# 121表示一行两列的子图中的第一个
plotKMeans(x, y, kmeans.centroids, 121, 'Initial State')

# 开始聚类
kmeans.fit(x)

plotKMeans(x, y, kmeans.centroids, 122, 'Final State')


# 预测数据点的类别
x_new = np.array([[0, 0], [10, 7]])
y_pred = kmeans.predict(x_new)

print(kmeans.centroids)
print(y_pred)

plt.scatter(x_new[:, 0], x_new[:, 1], s=100, c='black')
plt.show()


