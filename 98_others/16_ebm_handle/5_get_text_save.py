import os
import re
from pathlib import Path



# region
# 文件处理

# 获取输出文件路径 和 文字块标题
def get_names_obj(ori_path):
  path_arr = ori_path.split('\\')
  length = len(path_arr)
  path = fr"{path_arr[length - 3]}/{path_arr[length - 2]}.txt"
  title = path_arr[length - 1]
  return path, title

# 获取指定目录下所有目标后缀名文件
def find_files_by_extension_gen(root_dir, extensions):
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      if any(file.lower().endswith(ext.lower()) for ext in extensions):
        yield os.path.join(root, file)

# 合并文件并保存
def save_in_one_file(export_dir, ori_path):
  path, title = get_names_obj(ori_path)
  # print(fr"./{export_dir}/{path}")
  # print(title)
  text = ebm_to_text(ori_path, title)
  save_text(text, fr"./{export_dir}/{path}")
  
# endregion



# region
# ebm处理

# 打开ebm字节文件
def ebm_to_text(file_name, title):
  with open(file_name, 'rb') as binfile:
    data = binfile.read()

    # text = get_text_data(data)
    text = get_text_data(data, title)
  # print(text)
  return text


# # 保存文字到文件
def save_text(text, output_file):
  output_path = Path(output_file)
  # 自动创建父目录（如果不存在）
  output_path.parent.mkdir(parents=True, exist_ok=True)
  
  with open(output_file, 'a', encoding='utf-8') as fp:
    fp.write(text)
  


# 获取可读文字块的结束位置
def get_end_pos(bin, pos):
  i = pos
  while (True):
    # 结束位为0
    if (bin[i] == 0):
      return i
    i += 0x01


# 判断当前chunk是否是需要的可读文字块
def is_skip_chunk(chunk):
  if (len(chunk) == 4):
    # 后2位为FF也属于间隔块
    if(chunk[0] == 0xff and chunk[3] == 0xff):
      return True
    # 后2位为0
    elif(chunk[2] == 0 and chunk[3] == 0):
      return True
  return False


# 转换字节文件为可读文字
def get_text_data(binary_data, title):
  # 文本序号标识
  index = 1
  # 字节文件长度
  length = len(binary_data)
  # 字节序列
  filtered_bytes = bytearray()
  # 当前位置
  pos = 0x00
  # 可读文字块结束位置
  end_pos = 0
  # 添加对应文件标题
  filtered_bytes.extend(f"{title} ".encode('ascii') + b'\n')
  while (pos < length):
    # 第1位不为0时才可能是需要的文字块 
    if not (binary_data[pos] == 0):
      # 取4字节
      chunk = binary_data[pos: pos + 0x04]
      # print(chunk)
      if (is_skip_chunk(chunk)):
        pos += 0x04
        continue
      else:
        end_pos = get_end_pos(binary_data, pos)
        # 添加换行符
        chunk = binary_data[pos : end_pos] + b'\n'
        filtered_bytes.extend(chunk)
        pos = end_pos
        index += 1
    pos += 0x01
  
  # 解码为UTF-8
  text = filtered_bytes.decode('utf-8', errors='ignore')
  
  # 替换除换行符(\n)以外的控制字符 和 <CR> 字符串
  text = re.sub(r'[\x00-\x09\x0B-\x1F]+|<CR>', ' ', text).strip()
  text += '\n\n'
  return text

# endregion





def main():
  # 统计文件数量
  count = 0
  
  # 源目标根目录文件夹
  root_dir = "ebm"
  # 输出根目录文件夹
  export_path = "export"
  
  for file_path in find_files_by_extension_gen(fr"./{root_dir}", [".ebm"]):
    # print(file_path)
    save_in_one_file(export_path, file_path)
    count += 1
    
  print(count)
  


if __name__ == '__main__':
  main()
