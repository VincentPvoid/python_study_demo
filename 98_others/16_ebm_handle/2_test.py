import re

# 保存文字到文件
def save_text(str, output_file='output'):
  with open(f"./{output_file}.txt", 'a', encoding='utf-8') as fp:
    fp.write(str)


def get_text(binary_data):

  filtered_bytes = bytearray()
  length = len(binary_data)
  # 每次取4字节遍历
  for i in range(20, length, 4):
    chunk = binary_data[i:i + 4]
    # 检查后3字节是不为0
    if not (len(chunk) == 4 and (chunk[1] == 0 and chunk[2] == 0 and chunk[3] == 0)):
      filtered_bytes.extend(chunk)
    elif chunk == b'\x3C\x43\x52\x3E':
      continue

  # 尝试解码为ASCII或UTF-8
  try:
    text = filtered_bytes.decode('ascii')
  except UnicodeDecodeError:
    text = filtered_bytes.decode('utf-8', errors='ignore')

  # 清理非打印字符和多余空格
  text = re.sub(r'[\x00-\x1F]+', ' ', text).strip()
  return ' '.join(text.split())


def get_end_pos(bin, pos):
  i = pos
  while (True):
    # print("===")
    # print(bin[i])
    # print("===")
    if (bin[i] == 0):
      return i
    i += 0x01

def is_skip_chunk(chunk):
  if (len(chunk) == 4):
    if(chunk[0] == 0xff and chunk[3] == 0xff):
      return True
    elif(chunk[2] == 0 and chunk[3] == 0):
      return True
  return False
    
def get_text_data(binary_data):
  index = 1
  length = len(binary_data)
  filtered_bytes = bytearray()
  end_pos = 0
  pos = 0x20
  print(length)
  while (pos < length):
    # print(binary_data[pos])
    if not (binary_data[pos] == 0):
      chunk = binary_data[pos: pos + 0x04]
      # print(chunk)
      if (is_skip_chunk(chunk)):
        pos += 0x04
        continue
      else:
        # pos = get_tar_text(binary_data, pos, filtered_bytes)
        end_pos = get_end_pos(binary_data, pos)
        chunk =  f"{index} ".encode('ascii') + b'\n' + binary_data[pos : end_pos] + b'\n'
        filtered_bytes.extend(chunk)
        print("===")
        print(chunk)
        print("===")
        # filtered_bytes.extend()
        pos = end_pos + 0x01
        index += 1
        continue
    pos += 0x01
    
  # 尝试解码为ASCII或UTF-8
  try:
    text = filtered_bytes.decode('ascii')
  except UnicodeDecodeError:
    text = filtered_bytes.decode('utf-8', errors='ignore')

  # 替换除换行符(\n)以外的控制字符；同时替换文本中的<CR>字符串
  text = re.sub(r'[\x00-\x09\x0B-\x1F]+|<CR>', ' ', text).strip()
  return text

def test1(file_name):
  with open(f"./{file_name}.ebm", 'rb') as binfile:
      # print(binfile.read())
    # print(get_text(binfile.read()))
    # print(get_text_data(binfile.read()))
    return get_text_data(binfile.read())


if __name__ == '__main__':
  file_name = "EVENT_MESSAGE_040"

  str = test1(file_name)

 
  print(str)

  # save_text(str)
