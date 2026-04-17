import os




# 打开原始fp文件
def open_fp_file(file_name):
  with open(f"./{file_name}", 'rb') as binfile:
    data = binfile.read()

    # text = get_text_data(data)
    list = split_to_list(data)
  # print(list)
  print(len(list))

  # with open('list_output.txt', 'w', encoding='utf-8') as f:
  #   for item in list:
  #     f.write(str(item) + '\n')
  return list



# 获取指定目录下所有目标后缀名文件
def find_files_by_extension_gen(root_dir, extensions):
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      if any(file.lower().endswith(ext.lower()) for ext in extensions):
        # yield os.path.join(root, file)
        yield os.path.join(file)



# 判断是否为文件开头/结尾
# def is_file_symbol(chunk, check_name):
#   # 文件开头为KOVS（4B4F5653）
#   if (check_name == 'start'):
#     return chunk == b'KOVS'
#   else:
#     # 文件结尾为0E00000000
#     # check_name == 'end'
#     return chunk == b'\x0E\x00\x00\x00\x00'


# 分割文件为kovs文件块
def split_to_list(ori_data):
  list = []
  length = len(ori_data)

  # 字节序列，方便后面处理
  filtered_bytes = bytearray()

  # 当前位置
  pos = 0

  # 开始位置
  pos_start = 0
  # 结束位置
  pos_end = 0
  while (pos < length):
    if (ori_data[pos] == 0x4B):
      chunk = ori_data[pos: pos + 4]
      # 文件开头为KOVS（4B4F5653）
      if (chunk == b'KOVS'):
        # 结尾字符不固定，因此根据开头来判定；中间分隔的00很多数量不固定，因此直接往前数8位
        pos_end = pos - 8
        
        if (pos_end > 0):
          # 这里截取的是当前pos所在开头的前一个文件，即pos_start为上一个文件的开头
          tar = ori_data[pos_start: pos_end]
          filtered_bytes.extend(tar)
          list.append(tar)
          # 截取后再移到当前文件的开头，为下一次截取作准备
          pos_start = pos
        # 为开头的话直接跳过前面32位
        pos += 32
        continue
    pos += 1
  
  # 最后一个文件，截取到原始文件末尾
  # pos_end还停留在上一个文件末尾，因此加8位就为最后一个文件的开头；或者直接使用pos_start
  tar = ori_data[pos_end + 8: pos - 8]
  filtered_bytes.extend(tar)
  list.append(tar)

  return list


# 解密分割后的文件块
def decrypt_kovs_to_ogg(kovs_data, index_str, fp_file_name):
  # 跳过前 32 字节的 KOVS 容器头 (4B 4F 56 53...)
  payload = bytearray(kovs_data[32:])

  # 异或加密只有前256字节，后面是明文音频数据；因此对于超出这个长度的文件只取前256字节
  encryption_limit = min(256, len(payload))

  # 进行异或解密
  for i in range(encryption_limit):
    payload[i] ^= (i % 256)
    
  
  # 根据原文件名分文件夹
  output_dir = f"./output/{fp_file_name}"
  # 确保output文件夹存在
  os.makedirs(output_dir, exist_ok=True)

  output_filename = f"voice_{index_str}"
  
  # 写入为正常的 Ogg 文件
  with open(f"{output_dir}/{output_filename}.ogg", 'wb') as f:
    f.write(payload)
  print(f"file saved: {output_dir}/{output_filename}.ogg")


def main():
  ori_dir = 'ori_files'
  # ori_file_list = open_fp_file("xxx.fp")
  for fp_file_name in (find_files_by_extension_gen(f"./{ori_dir}", [".fp"])):
    ori_file_list = open_fp_file(f"./{ori_dir}/{fp_file_name}")
    for i, item in enumerate(ori_file_list):
      index_str = f"{i:03d}"  # 格式化3位，不足补0
      decrypt_kovs_to_ogg(item, index_str, fp_file_name)


if __name__ == '__main__':
  main()
