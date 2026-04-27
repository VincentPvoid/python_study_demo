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
    i += 1



# 转换字节文件为可读文字
def get_text_data(binary_data, title):
  # 字节文件长度
  length = len(binary_data)
  filtered_bytes = bytearray()
  # 每个文件开头有4字节的其他数据，先跳过这一段，新文件直接从第5位开始找
  pos = 4
  end_pos = 0
  filtered_bytes.extend(f"{title} ".encode('ascii') + b'\n')
  while (pos < length):
    # 取前36位，获取标识符等信息
    chunk = binary_data[pos : pos + 36]
    # 角色标识
    char_id = int.from_bytes(chunk[4 : 4 + 4], byteorder='little')
        
    # 文本序号
    text_index = int.from_bytes(chunk[24 : 24 + 4], byteorder='little')   
    prefix = f"[num: {text_index}] [char_id: {char_id}] : ".encode('utf-8')
    
    pos += 36
    
    if(pos >= length):
      break
    
    end_pos = get_end_pos(binary_data, pos)
    chunk = prefix + binary_data[pos : end_pos] + b'\n'
    filtered_bytes.extend(chunk)
    pos = end_pos + 1
  
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
    print(file_path)
    save_in_one_file(export_path, file_path)
    count += 1
    
  print(count)
  


if __name__ == '__main__':
  main()
