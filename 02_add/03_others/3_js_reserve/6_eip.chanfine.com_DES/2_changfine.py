import execjs


node = execjs.get()
ctx = node.compile(open('./1_des.js', encoding='UTF-8').read())
# print(type(ctx))
funcStr = 'getPwd("{0}")'.format('123')
pwd = ctx.eval(funcStr)
print(pwd)