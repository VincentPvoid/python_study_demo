# a = [1,2]
# b = [1,2,3]


# for i in range(len(a), len(b)):
#   print(b[i])

# import time
from dateutil import parser

time_str = '21 Aug, 2012'
datetime_struct = parser.parse(time_str)
print(type(datetime_struct)) # <type 'datetime.datetime'>
print(datetime_struct.strftime('%Y-%m-%d %H:%M:%S')) # 2012-08-21 00:00:00

