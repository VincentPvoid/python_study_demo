import execjs

# 1. 实例化一个node对象
node = execjs.get()

# 2. 对js源文件进行编译
ctx = node.compile(open('./1_base.js', encoding='utf-8').read())

# 3. 执行js函数
funcName = 'getPwd("{0}")'.format('123')
pwd = ctx.eval(funcName)
print(pwd) # 202cb962ac59075b964b07152d234b70
