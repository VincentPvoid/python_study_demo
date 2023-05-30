import jieba
# 注意jieba.analyse要单独引入，否则报错
import jieba.analyse

# 导入词云插件
from wordcloud import WordCloud

# 导入自定义词表
jieba.load_userdict("./dict/cus_dict.txt")

# 把文档中的句子拆分为词语
def cut_words():
  text_str = ''
  with open('./target_normal.txt', mode='r', encoding='utf-8') as fp:
    for line in fp:
      # print(list(jieba.cut(line.strip())))
      # 注意jieba.cut方法返回的是一个generator迭代器；遍历完一次就不能再取出
      # temp = jieba.cut(line.strip())
      
      # 使用jieba.lcut方法可直接返回一个列表
      text_list = jieba.lcut(line.strip())
      # print(text_list)  
      text_str += ' '.join(text_list).strip()
  return text_str

# 根据拆分好的字符串生成词云
def get_wordcloud(ori_str):
  # str = ori_str

  # 使用jieba分析出现频率最高的词
  # 基于 TF-IDF 算法的关键词抽取（根据文本本身计算，因为不是特定语料库所以权重计算全靠原文档）
  # str = jieba.analyse.extract_tags(ori_str, topK=100, withWeight=False, allowPOS=())
  # str = ' '.join(str)

  # 基于 TextRank 算法的关键词抽取
  str = jieba.analyse.textrank(ori_str, topK=100, withWeight=False)
  str = ' '.join(str)

  # 如果数据文件包含有中文，font_path必须指定字体，否则中文会乱码
  # collocations 是否包括两个词的搭配，默认为True；为True时会有重复数据
  # width，height 词云图的宽高
  # max_words 显示词的最大个数
  # generate 需要读取的字符串
  wordcloud = WordCloud(font_path='C:/Windows/Fonts/msyh.ttc',
                        collocations=False,
                        width=500,
                        height=400,
                        max_words=60,
                        background_color="white"
                        ).generate(str)
  # 生成图片
  image = wordcloud.to_image()
  # 展示图片
  # image.show()
  # 写入文件
  wordcloud.to_file('normal_words.jpg')


if __name__ == '__main__':
  # 获取以空格拆分的字符串
  str = cut_words()
  # print(str)
  # print(jieba.analyse.textrank(str, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')) )
  # 使用jieba分析出现频率最高的词
  # print(jieba.analyse.extract_tags(str, topK=60, withWeight=True, allowPOS=()))
  # print(len(jieba.analyse.textrank(str, topK=60, withWeight=True)))
  get_wordcloud(str)




