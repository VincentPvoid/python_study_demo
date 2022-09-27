import sys
sys.path.append("D:\Python\Python310\Lib\site-packages")


# jsonpath的使用：
# obj = json.load(open('json文件', 'r', encoding='utf‐8'))
# ret = jsonpath.jsonpath(obj, 'jsonpath语法')
# 注意：与xpath不同，jsonpath只能解析本地文件

import json
import jsonpath

obj = json.load(open('./testData/booksJson.json', 'r', encoding="utf-8"))

# 该文件中所有的作者
# authors_list = jsonpath.jsonpath(obj, '$.store.book[*].author')

# 所有的作者
# authors_list = jsonpath.jsonpath(obj, '$..author')
# print(authors_list) 

# store下所有的元素
# tags_list = jsonpath.jsonpath(obj, '$.store.*')
# print(tags_list)


# store下所有的price
# price_list = jsonpath.jsonpath(obj, '$.store..price')
# print(price_list)

# 第三本书
# book3 = jsonpath.jsonpath(obj, '$.store.book[2]')
# print(book3)

# 最后一本书
# last_book = jsonpath.jsonpath(obj, '$.store.book[(@.length-1)]')
# print(last_book)

# 前面两本书
# books = jsonpath.jsonpath(obj, '$..book[0,1]')
# books = jsonpath.jsonpath(obj, '$..book[:2]')
# print(books)

# 条件过滤需要在()前加?
# 注意：如果没有符合条件的值，则会返回 False，而不是空列表（数组）
# 所有包含ISBN的书
# books_list = jsonpath.jsonpath(obj, '$..book[?(@.isbn)]')

# 所有价格低于10的书
books_list = jsonpath.jsonpath(obj, '$..book[?(@.price<10)]')
print(books_list)