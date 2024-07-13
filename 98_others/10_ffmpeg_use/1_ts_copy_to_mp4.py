import os

# 使用ffmpeg，把ts文件重新复制打包为mp4文件
def ts_cto_mp4(ts_file_path, ts_file_name, out_path):
  tar_file = f"{out_path}\\{ts_file_name}.mp4"
  cmd_str = f"ffmpeg -i {ts_file_path} -acodec copy -vcodec copy -f mp4 {tar_file}"
  print(cmd_str)
  try:
    # 执行命令
    os.system(cmd_str)
  except Exception as e:
    print(e)
  print("finish")



def main():
  # 原始视频文件目录
  folder_path = "ori file path"
  
  # 输出文件目录
  out_path = "out file path"
  
  # 原始视频文件名称列表
  file_name_list = []
  
  # 遍历文件夹中的文件
  for file_name in os.listdir(folder_path):
    # 检查文件后缀是否为ts文件
    if file_name.endswith('.ts'):
      # 获取集数文字；该操作用于过滤相同的文件
      temp = file_name.split('.ts')[0]
      # 如果当前列表不存在该集数
      if temp not in file_name_list:
        file_name_list.append(temp)

        # 获取ts文件的完整路径
        ts_file_path = os.path.join(folder_path, file_name)
        
        ts_cto_mp4(ts_file_path, temp, out_path)
  
if __name__ == '__main__':
  main()  
