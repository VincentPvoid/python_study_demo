# TD-IDF算法实例

import pandas as pd
import math


# 1. 定义数据和预处理
doc_a = 'The cat set on my bed'
doc_b = 'The dog set on my knees'

# 把各个句子拆分为单独的词
bow_a = doc_a.split(' ')
bow_b = doc_b.split(' ')

# 构建词库；把所有词去重放入set集合中
word_set = set(bow_a).union(bow_b)
print(word_set)


# 2. 进行词数统计
# 用统计字典来保存词出现的次数
# dict.fromkeys() 把word_set中的值作为key，生成值全为0的字典
word_dict_a = dict.fromkeys(word_set, 0)
word_dict_b = dict.fromkeys(word_set, 0)

# 遍历文档，统计词数
for word in bow_a:
  word_dict_a[word] += 1
for word in bow_b:
  word_dict_b[word] += 1

# df = pd.DataFrame([word_dict_a, word_dict_b])
# print(df)


# 3. 计算TF词频
def computeTF(word_dict, bow):
  # 用一个字典对象记录tf，把所有的词对应在bow文档里的tf都算出来
  tf_dict = {}
  # 文档词语总数
  n_count_num = len(bow)
  # 遍历对应的字典
  for word, count in word_dict.items():
    # 计算词频
    tf_dict[word] = count / n_count_num
  return tf_dict

tf_a = computeTF(word_dict_a, bow_a)
tf_b = computeTF(word_dict_b, bow_b)

# print(tf_a)
# print(tf_b)



# 4. 计算IDF逆文档频率
def computeIDF(word_dict_list):
  # 用一个字典对象保存idf结果，每个词作为key，初始值为0
  # word_dict_list就是两个文档对应的次数统计字典，因为两个字典之前设定的key都相同（为全部的词）
  # 所以可以直接使用其中一个的key生成新的字典对象
  idf_dict = dict.fromkeys(word_dict_list[0], 0)
  N = len(word_dict_list)
  
  for word_dict in word_dict_list:
    # 遍历字典中的每个词汇，统计Ni
    # Ni表示所有文档中，包含某个词的文档数（在某一个文档中重复出现也只记录为1次）
    for word, count in word_dict.items():
      if(count > 0):
        idf_dict[word] += 1

  for word, ni in idf_dict.items():
    # 已经得到所有词汇i对应的Ni，现在根据公式把它替换成为idf值
    idf_dict[word] = math.log10((N + 1) / (ni + 1))

  return idf_dict

idfs = computeIDF([word_dict_a, word_dict_b])
print(idfs)


# 5. 计算TF-IDF 词频-逆文档频率
# TFIDF = TF x IDF
def computeTFIDF(tf, idfs):
  tfidf = {}
  # 统计某个文档中对应词的TF-IDF
  for word, tfval in tf.items():
    tfidf[word] = tfval * idfs[word]
  return tfidf

tfidf_a = computeTFIDF(tf_a, idfs)
tfidf_b = computeTFIDF(tf_b, idfs)

print(pd.DataFrame([tfidf_a, tfidf_b]))


