# 使用pandas来分析数据
import pandas as pd

# pandas设置
# # 不限制最大显示列数
# pd.set_option('display.max_columns', None)
# 不限制最大显示行数；如果不设置可能中间会省略，显示不完整
pd.set_option('display.max_rows', None)
# 不使用科学计数法显示数据
# pd.set_option('display.float_format', lambda x: '%.3f' % x)


# header=None表示不使用第一行作为列名；pandas会自动添加序号作为列名
data = pd.read_csv('movie_box_offset.csv', header=None)
# print(data)

# 获取需要的列数；:表示所有行，[2,3]表示3,4列
# data = data.loc[:, [2, 3]]
# data = data.loc[:, 1:4] # 表示获取所有行和2-5列数据

# 获取需要的数据；所有列和下标为3-5的列
# data = data.loc[:, 3:5]
# print(data)

# 获取 3电影类型 和 5票房数据 列
# data = pd.DataFrame(data, columns=[3,5])
data = data.loc[:, [3,5]]


# df = pd.DataFrame(data, columns=[5,6,7,8])
# 合并列操作；需要先把所有列的数据转换为字符串
# df = df.astype(str)
# df = df.loc[df[8] != 'nan'] # 该操作为去除含有nan的行（不需要该操作）
# box_offset = df[5] + df[6] + df[7] + df[8]
# print('==============')
# print(box_offset)

# print(data)


# 拆分数据（拆分电影类型）

# 获取第一个电影类型函数
def first_type(str):
  return str.split('/')[0]

# 获取第二个电影类型函数；可能为空，当为空时可以自定义填充其他值，方便后续处理
def second_type(str):
  if(str.find('/')!=-1):
    return str.split('/')[1]
  else:
    return 'nodata'

# 把拆分的数据放入data中下标为6 7的列中
data[6] = data[3].map(first_type)
data[7] = data[3].map(second_type)

# print(data)

# 用拆分出来的数据分别生成2个表
temp_1 = data.loc[:, [6,5]]
temp_2 = data.loc[:, [7,5]]
# 去除表2中没有类别（该项值为nodata)的行
temp_2 = temp_2.loc[temp_2[7] != 'nodata']
# print(temp_1)
# print(temp_2)

# 表1中没有下标为7的列，表2中没有下标为6的列，
# 如果直接合并，对应不存在的列会生成NaN数据，没有达到合并表的效果
# 所以需要先把某个表的列重命名再进行合并；该例子中是把表2的下标为7的列重命名为6
temp_2 = temp_2.rename(columns={7:6})
# 合并两个表
# data = temp_1.append(temp_2)
data = pd.concat([temp_1, temp_2])

# 票房数据含有$和,符号，需要进行去除
# （该例子中数据过大，为了方便处理所以进行了截取；只作为练习演示所以可以这样操作）
def get_box_offset_num(str):
  # return int(str.split('$')[0].replace(',', ''))
  temp = str.split('$')[0].replace(',', '')
  temp = temp[:6]
  return int(temp)

data[5] = data[5].map(get_box_offset_num)

# 计算每一种类型的票房平均值；
# groupby()表示用第x列数据进行分组；mean()计算平均值；round()截取指定位数小数
# res = data[5].groupby(data[6]).mean().round(2)
# res = data.groupby(6).mean().round(2)

# 重命名数据列
# data = data.rename(columns={6:'type', 5:'box_offset'})
data = data.rename(columns={6:'name', 5:'value'})
res = data.groupby('name').mean().round(2)

# print(res)

# 把处理后的数据保存到文件中
res.to_csv('classify_data.csv')

