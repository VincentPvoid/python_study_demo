import re


# 帧数转时间
def frame_num_to_time(ori_frame_num, framerate=23.98):
  res = ""
  # 帧数转总秒数
  second = int(ori_frame_num) / framerate

  # 把小数转换为整数，并进行补0
  hour = str(int(second / 3600)).zfill(2)
  min = str(int(second / 60 % 60)).zfill(2)
  s = str(int(second % 60)).zfill(2)
  ms = str(int(second * 1000 % 1000)).zfill(3)

  # 秒数转换为HH:mm:ss,xxx格式
  res = f'{hour}:{min}:{s},{ms}'
  # print(res)
  return res


# 获取对应时间和文字列表
def get_list():
  # 提取帧数数字正则
  reg_num = re.compile('[0-9]+')

  # list中的对象格式{time:[开始时间, 结束时间], text:对应文字}
  list = []
  with open('./ori_sub/ori.sub', mode="r", encoding="utf-8") as fp:
    for line in fp:
      # 提取文字
      text = line.split('}')[2].strip()
      temp_arr = re.findall(reg_num, line)
      # print(temp_arr)
      obj = {
          'text': text,
          'time':
          [frame_num_to_time(temp_arr[0]),
           frame_num_to_time(temp_arr[1])]
      }
      list.append(obj)
  # print(list)
  return list


# 把文件保存为srt文件
def save_srt_file(data_list, file_name):
  with open(file_name + '.srt', "w", encoding='utf-8') as f:
    # for obj in data_list:
    for i, obj in enumerate(data_list):
      # print(i, obj)
      text = f'{i+1}\n{obj["time"][0]} --> {obj["time"][1]}\n{obj["text"]}\n\n'
      f.write(text)


def main():
  data_list = get_list()
  save_srt_file(data_list, 'target')

if __name__ == '__main__':
  main()