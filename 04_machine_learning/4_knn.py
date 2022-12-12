# k近邻算法

import numpy as np
import pandas as pd

# 直接引入sklearn里的数据集，iris莺尾花
from sklearn.datasets import load_iris
# train_test_split()切分数据集为训练集和测试集
from sklearn.model_selection import train_test_split
# accuracy_score()计算分类预测的准确率
from sklearn.metrics import accuracy_score



# 1. 数据加载和预处理
iris = load_iris()
# print(iris)

# pd设置，不限制最大显示行数
pd.set_option('display.max_rows', None)
# data数据 columus列名
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)

# pandas可以直接添加新的列
df['class'] = iris.target
# 使用map处理某列的值，替换为对应的值；如果没有对应值，则会显示为NaN
df['class'] = df['class'].map({
  0: iris.target_names[0],
  1: iris.target_names[1],
  2: iris.target_names[2],
})
# print(df)

# describe()数据统计信息；
# count总数 mean平均值 std标准方差 min最小值 max最大值 处于25%/50%（中位数）/75%位置的数
# print(df.describe())

# 二维嵌套数据
x = iris.data
# 原数据为一维数组，需要转换为嵌套的二维数组（后续操作时参数要求为矩阵形式）
y = iris.target.reshape(-1, 1)
# print(y)
# print(x.shape, y.shape) # (150, 4) (150, 1)


# 划分训练集和测试集
# test_size 测试集占总输入数据的比例
# random_state 随机数种子；每次都设置为相同的值时，会得到相同的随机值；这里设置是为了保证在相同的数据情况下，每次执行代码时都能得到相同的训练集和测试集
# stratify 按照给定的参数，保持比例分割数据；这里填y表示按照y中的比例分配；该例子中表示分割后的数据集中需要有同样比例的0、1、2分布
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=35, stratify=y)

# 训练集矩阵形状
print(x_train.shape, y_train.shape) # (105, 4) (105, 1)
# 测试集矩阵形状
print(x_test.shape, y_test.shape) # (45, 4) (45, 1)

# print(x_test)

# 该方法要求减数的行数为1，所以不能直接相减
# print(np.abs(x_train-x_test))

# 取x_text的其中一行，转换为(1,4)形式的二维数组；该结果可以作为减数进行计算；计算后的结果为(105,4)形式的二维数组
# 或是转换为相同个数（4）的一维数组，也可以作为减数进行计算
# print(x_test[0].reshape(1, -1))

# axis默认为None，因此结果为所有数值相加 387.4
# 以下两种写法结果相同
# print(np.sum(np.abs(x_train-x_test[0].reshape(1,-1))))
# print(np.sum(np.abs(x_train-x_test[0])))

# 结果为(104,)的一维数组
# 以下两种写法结果相同
# print(np.sum(np.abs(x_train-x_test[0].reshape(1,-1)), axis=1))
# print(np.sum(np.abs(x_train-x_test[0]), axis=1))




# 2. 核心算法实现

# 定义距离函数
# 曼哈顿距离
def l1_distance(a, b):
  return np.sum(np.abs(a-b), axis=1)

# 欧式距离
def l2_distance(a, b):
  return np.sqrt(np.sum((a-b)**2, axis=1))


# 分类器实现
class kNN(object):
  # 定义一个初始化方法；__init__是类的构造方法
  # 都需要传入self参数，指代类的实例；类似js中的this
  # n_neighbors 近邻数量；默认设置为1
  # dist_func 距离函数
  def __init__(self, n_neighbors = 1, dist_func = l1_distance):
    # 把参数传到实例的属性中
    self.n_neighbors = n_neighbors
    self.dist_func = dist_func

  # 训练模型方法
  def fit(self, x, y):
    self.x_train = x
    self.y_train = y

  # 模型预测方法
  def predict(self, x):
    # 初始化预测分类数组
    # 求出的预测值结果，行数应该与x相同，列数与y_train相同（该例子中为1）
    # np.zeros()初始化一个值全为0的数组；
    # 第一个参数为设置结果的形状；（该例子中为x_test）
    # dtype参数为设置结果的数据类型，默认为浮点型；该例子中设置为与原来的y_train值相同
    y_pred = np.zeros( (x.shape[0],1), dtype=self.y_train.dtype)

    # 遍历输入的x数据；使用enumerate()方法获取下标和对应数值
    for i, x_test in enumerate(x):
      # x_test与所有训练数据计算距离
      # 结果格式[x, x, x, ...]，总长度与x的测试集相同的数组
      distance = self.dist_func(self.x_train, x_test)

      # 按照从近到远（从小到大）的顺序排列得到的距离结果，获取对应的索引值排序
      # np.argsort()根据值的大小进行排序，返回排序后对应的下标索引
      nn_index = np.argsort(distance)

      # 选取与当前的x数据最近的k个点，保存它们对应的分类类别（y_train）
      # 当前数据为x_test中的值，找到距离最近的x_train值对应的y_train值
      # 因为y_train是二位嵌套数组，所以获取到的值也是二维嵌套数组形式；
      # 为了方便计算，可以使用reval()方法展开数组（把数组变为一维形式）
      nn_y = self.y_train[nn_index[:self.n_neighbors]].ravel()

      # 统计对应类别中出现频率最高的数据，赋值给y_pred[i]
      # bincount()计算出现频率最高的数据（因为数据值为0,1,2这样的值，所以适用此方法）
      # argmax() 返回值最大的数据对应的下标值
      y_pred[i] = np.argmax(np.bincount(nn_y))

    return y_pred




# 3. 测试

# 定义一个knn实例
knn = kNN(n_neighbors = 3)
# 训练模型
knn.fit(x_train, y_train)
# 传入测试数据，获取预测值（y_pred)
y_pred = knn.predict(x_test)
# 计算预测准确率
accuracy = accuracy_score(y_test, y_pred)

# print(accuracy)


# 改变参数计算预测准确率
# 定义一个knn实例
knn = kNN()
# 训练模型
knn.fit(x_train, y_train)
# 保存预测结果的列表
res_list = []

# 改变参数作预测
for p in [1, 2]:
  if p == 1:
    knn.dist_func = l1_distance
  else:
    knn.dist_func = l2_distance
  
  # 简便写法；效果与上面写法相同
  # knn.dist_func = l1_distance if p == 1 else l2_distance
  
  
  # 不同k的取值，步长为2；一般情况下，k值都设定为奇数
  for k in range(1, 10, 2):
    knn.n_neighbors = k
    # 输入测试数据进行预测
    y_pred = knn.predict(x_test)
    # 计算预测准确率
    accuracy = accuracy_score(y_test, y_pred)
    # 把每次获取的准确率存入结果列表中；
    # 为了方便查看对应的参数，把对应的参数也存入结果列表中
    res_list.append([k, 'l1_distance' if p == 1 else 'l2_distance', accuracy])

# print(res_list)

# 为了方便查看，生成表格
df = pd.DataFrame(data=res_list, columns=['k', 'dist_func', 'accuracy'])
print(df)
