import os

# 合并音视频
def merge_video_audio(video_name, audio_name):
  cmd_str = f"ffmpeg -i {video_name}.mp4 -i {audio_name}.mp3 -c:v copy -c:a aac -strict experimental {video_name}_output.mp4"
  print(cmd_str)
  try:
    # 执行合并命令
    os.system(cmd_str)
  except Exception as e:
    print(e)
  print("merge finish")


def main():
  video_name = "./ori/mp4name"
  audio_name = "./ori/mp3name"
  merge_video_audio(video_name, audio_name)

if __name__ == '__main__':
  main()

