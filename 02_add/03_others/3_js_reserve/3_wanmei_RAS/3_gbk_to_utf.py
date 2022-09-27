# 转格式 
# 原本保存的js文件中含有python无法解析的\xa0字符串，需要进行去除，否则执行python时会报错

fp = open('./ras.js','r', encoding='UTF-8')

content = fp.readlines()

res = "".join(content)

# 替换文本字符串中的\xa0为普通空格
res = res.replace(u'\xa0', u' ')
# res = "".join(res.split())

# print(res)

fp.close()

fp = open('./1_ras.js','w', encoding='UTF-8')
fp.write(res)
fp.close()
