# a = [1,2]
# b = [1,2,3]


# for i in range(len(a), len(b)):
#   print(b[i])

# import time
# from dateutil import parser

# time_str = '21 Aug, 2012'
# datetime_struct = parser.parse(time_str)
# print(type(datetime_struct)) # <type 'datetime.datetime'>
# print(datetime_struct.strftime('%Y-%m-%d %H:%M:%S')) # 2012-08-21 00:00:00



import re
import requests
import json

url = 'https://store.steampowered.com/app/xxxxx/'
steamcmd_url = re.sub('store.steampowered.com/app', 'api.steamcmd.net/v1/info', url)
steam_app_id = url.rstrip("/").split("/")[-1] 

print(url)
print(steamcmd_url)
print(steam_app_id)


# def build_string_from_dict(obj, tar_list):
#   text = ""
#   for item in tar_list:
#     for key, value in item.items():
#       if key in obj and obj[key]:
#         text += f"[{value}|{obj[key]}]\n"
#   return text

# test_obj = {
# }

# tar_list = [{'tchinese':'繁中'}, {'japanese':'日文'}, {'koreana':'韩文'}]

# print(build_string_from_dict(test_obj, tar_list))

test_url = 'https://api.steamcmd.net/v1/info/xxxxxxx'
response = requests.get(url=test_url)
response.encoding = 'utf-8'
print(json.loads(response.text))
# print(response.text['data'])