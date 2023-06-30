import zipfile
import os


# 解压缩
def un_zip(file_name, out_path):
  # 目标文件格式
  tar_type = '.srt'
  # 打开对应zip文件；注意需要完整路径
  zip_file = zipfile.ZipFile(file_name)
  # 获取对应zip文件中的文件名列表
  nl = zip_file.namelist()
  # print(nl)

  for fn in nl:
    # 如果为目标格式文件
    if fn.endswith(tar_type):
      # 解压缩文件到指定文件夹
      zip_file.extract(fn, out_path)
      
  # 处理完成后关闭zip文件
  zip_file.close()



def main():
  # zip文件目录
  folder_path = "your zip path"
  # 解压后文件目录
  out_path = "your un zip path"

  # zip文件名称列表；这里用于判断当前集数的字幕是否已经存在
  file_name_list = []

  # 遍历文件夹中的文件
  for file_name in os.listdir(folder_path):
    # 检查文件后缀是否为zip文件
    if file_name.endswith('.zip'):
      # 获取集数文字；该操作用于过滤相同的文件；文件名格式xxxxx SxxExx name.xxx.xxx.zip
      temp = file_name.split(" ")[4]

      # 如果当前列表不存在该集数
      if temp not in file_name_list:
        file_name_list.append(temp)

        # 获取zip文件的完整路径
        zip_file_path = os.path.join(folder_path, file_name)

        un_zip(zip_file_path, out_path)

      

if __name__ == '__main__':
  main()