import re


# 打开ebm字节文件
def ebm_to_text(file_name):
  with open(f"./{file_name}.ebm", 'rb') as binfile:
    data = binfile.read()

    # text = get_text_data(data)
    text = get_text_data(data)
  print(text)
  return text

# 保存文字到文件
def save_text(str, output_file='output'):
  with open(f"./{output_file}.txt", 'a', encoding='utf-8') as fp:
    fp.write(str)


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
def get_text_data(binary_data):
  # 文本序号标识
  index = 1
  # 字节文件长度
  length = len(binary_data)
  # print(length)
  # 字节序列
  filtered_bytes = bytearray()
  # 当前位置
  pos = 0x00
  # 可读文字块结束位置
  end_pos = 0
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
        # 添加序号和换行符
        # chunk =  f"{index} ".encode('ascii') + b'\n' + binary_data[pos : end_pos] + b'\n'
        # 添加换行符
        chunk = binary_data[pos : end_pos] + b'\n'
        filtered_bytes.extend(chunk)
        print("===")
        print(chunk)
        print("===")
        pos = end_pos
        index += 1
        # continue
    pos += 0x01
    
  # 尝试解码为ASCII或UTF-8
  # try:
  #   text = filtered_bytes.decode('ascii')
  # except UnicodeDecodeError:
  #   text = filtered_bytes.decode('utf-8', errors='ignore')
  
  # 解码为UTF-8
  text = filtered_bytes.decode('utf-8', errors='ignore')
  
  # 替换除换行符(\n)以外的控制字符
  # text = re.sub(r'[\x00-\x09\x0B-\x1F]+', ' ', text).strip()
  # 替换文本中的<CR>字符串为换行符
  # text = re.sub(r'<CR>', '\n', text)
  
  # 替换除换行符(\n)以外的控制字符 和 <CR> 字符串
  text = re.sub(r'[\x00-\x09\x0B-\x1F]+|<CR>', ' ', text).strip()
  text += '\n\n'
  return text


if __name__ == '__main__':
  file_name = "EVENT_MESSAGE_040"

  str = ebm_to_text(file_name)

  print(str)

  save_text(str)
