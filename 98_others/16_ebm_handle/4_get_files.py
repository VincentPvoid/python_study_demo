import os
from pathlib import Path


def save_text(text, output_file):
  """使用 pathlib 安全写入文件"""
  output_path = Path(output_file)
  # 自动创建父目录（如果不存在）
  output_path.parent.mkdir(parents=True, exist_ok=True)
  
  temp_file = output_file + ".tmp"
  with open(temp_file, 'w', encoding='utf-8') as fp:
    fp.write(text)
  os.replace(temp_file, output_file)  # 原子操作（Python 3.3+）

  # # 写入文件
  # with output_path.open('a', encoding='utf-8') as fp:
  #   fp.write(text)



# 获取输出文件路径 和 文字块标题
def get_names_obj(ori_path):
  path_arr = ori_path.split('\\')
  length = len(path_arr)
  path = fr"{path_arr[length - 3]}\{path_arr[length - 2]}.txt"
  title = path_arr[length - 1]
  return path, title


# 获取指定目录下所有目标后缀名文件
def find_files_by_extension_gen(root_dir, extensions):
  """生成器版本，适用于大量文件"""
  for root, dirs, files in os.walk(root_dir):
    for file in files:
      if any(file.lower().endswith(ext.lower()) for ext in extensions):
        yield os.path.join(root, file)


def save_in_one_file(export_dir, ori_path):
  path, title = get_names_obj(ori_path)
  print(fr"./{export_dir}\{path}")
  print(title)


def main():
  count = 0
  export_path = "export"
  for file_path in find_files_by_extension_gen("./test", [".ebm"]):
    print(file_path)
    save_in_one_file(export_path, file_path)
    count += 1
  print(count)


if __name__ == '__main__':
  main()
