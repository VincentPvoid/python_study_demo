import pyautogui
import win32gui
import os
import time
import cv2
from PIL import Image
import pytesseract
import numpy as np
import re


# 获取当前路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 示例template图片路径
path = current_dir + "/example"

# 窗口位置偏移量
win_offset = 200

global_pos = (0,0)

# skill1按钮位置
skill_pos_left = 0
skill_pos_top = 0

# start按钮位置
start_pos_x = 0
start_pos_y = 0

# item按钮位置 x-L y-T
item_icon_pos_x = 50
item_icon_pos_y = 450

# 物品位置 x-R y-T
item_pos_x = 90
item_pos_y = 102

# 使用物品按钮位置 x-R y-B
item_use_pos_x = 236
item_use_pos_y = 54

# 物品菜单关闭按钮位置 x-R y-T
item_close_pos_x = 48
item_close_pos_y = 20




def get_tar_window():
   # 目标程序标题
  title = "レスレリアーナのアトリエ"
  # 获取目标窗口句柄
  hwnd = win32gui.FindWindow(None, title)
  # win32gui.GetWindowText(hwnd)
  # test_obj.update({hwnd: win32gui.GetWindowText(hwnd)})
  return hwnd


# 获取指定图片中间位置
def image_to_position(screen, template):
  screen = cv2.imread(f"{current_dir}/screenshot.png")
  image_x, image_y = template.shape[:2]
  result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
  print("prob:", max_val)
  if max_val > 0.93:
    # 中间位置
    pos = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
    return pos
  else:
    return (0, 0)


# 指定区域截图
def get_screenshot(x, y):
  # pyautogui.screenshot(f"{path}/screenshot.png",region=[x + lb, y + tb, 1280, 720])
  # screenshot = pyautogui.screenshot(region=[x + lb, y + tb, 1280, 720])
  screenshot = pyautogui.screenshot(region=[x, y, 1280, 720])
  screenshot.save(f"{current_dir}/screenshot.png")
  return screenshot


# 移动鼠标到屏幕指定位置
def mouse_move(x, y, duration=0.05):
  print("move: ", x, y)
  pyautogui.moveTo(x, y, duration=duration)


# 左键单击/双击，右键单击
def mouse_click(operation='click'):
  if (operation == 'click'):
    pyautogui.click()
  elif (operation == 'double'):
    pyautogui.doubleClick()
  elif (operation == 'right'):
    pyautogui.rightClick()


# 目标图片元素是否存在于当前截图画面中
def is_has_tar_img(screenshot, template_name, file_format = 'jpg'):
  # template = cv2.imread(f"{path}/{template_name}.jpg")
  template = cv2.imread(f"{path}/{template_name}.{file_format}")
  global global_pos
  global_pos = image_to_position(screenshot, template)
  if (global_pos[0] != 0):
    # print(global_pos)
    return True
  return False


# 点击skill1按钮
def click_skill1_button():
  mouse_move(skill_pos_left, skill_pos_top)
  mouse_click()

# 点击编成/出击按钮
def click_team_start(right, bottom):
  bottom_offset = 45
  right_offset = 45
  mouse_move(right - right_offset, bottom - bottom_offset)
  mouse_click()
  time.sleep(0.5)
  mouse_click()

# 点击A敌人位置
def click_enemy_A():
  print("AAAAA")
  mouse_move(left + 580, top + 25)
  mouse_click()

# 点击中间敌人位置
def click_enemy_T():
  print("TTTTT")
  mouse_move(left + 610, top + 20)
  mouse_click()


# 打开skill1菜单（需要先打开才能攻击）
def open_skill1_menu():
  print("++ open_skill1_menu")
  # 打开之前先把菜单关闭
  mouse_move(skill_pos_left, skill_pos_top - 70)
  mouse_click()
  click_skill1_button()

  
  # get_screenshot(left, top)
  # screenshot = f"{current_dir}/screenshot.png"
  # repetitions = 0
  # while (not is_has_tar_img(screenshot, 'skill1_active')):
  #   print("++ open_skill1_menu")
    
    
  #   repetitions += 1
  #   if(repetitions > 5):
  #     click_team_start(right - 50, bottom - 50)
  #     break


# 关闭skill1菜单
def close_skill1_menu():
  print("-- close_skill1_menu")
  mouse_move(skill_pos_left, skill_pos_top - 70)
  mouse_click()
  # get_screenshot(left, top)
  # screenshot = f"{current_dir}/screenshot.png"
  # repetitions = 0
  # # 如果菜单为打开状态则点击右下角
  # while (True):
  #   print("++ close_skill1_menu")
  #   click_team_start(right - 50, bottom - 50)    
  #   repetitions += 1
  #   if(repetitions > 3):
  #     click_skill1_button()
  #     break
  


# 持续点击右下角，直到进入战斗界面
def keep_click_brc():
  print("keep click bottom right corner")
  start_time = time.time()
  click_right = right - 45
  click_bottom = bottom - 45
  while (True):
    now_time = time.time()
    # 点击右下方
    # click_team_start(click_right, click_bottom)
    mouse_move(click_right, click_bottom)
    mouse_click()
    mouse_click("double")
    screenshot = get_screenshot(left, top)
    
    # 检测下一步按钮
    # if(is_has_tar_img(screenshot, 'next_btn', 'png')):
    #   click_right_times += 1
    #   mouse_click("right")
    #   if(click_right_times >= 2):
    #     mouse_move(right - 45 - 385, bottom - 45 - 32)
    #     mouse_click()
    #   continue
    
    # 检测skill1按钮是否存在
    if (is_has_tar_img(screenshot, 'skill1_normal')):
      break
    else:
      # 如果没有进入战斗界面，则移动一点位置再点击
      click_right -= 5
      click_bottom -= 2  
    # 如果超过10s还没有进入战斗界面
    if (duration_time(start_time, now_time) > 10):
      mouse_click("right")
      mouse_click("right")
      mouse_move(right - 45 - 385, bottom - 45 - 32)
      mouse_click()
      start_time = time.time()
      click_right = right - 45
      click_bottom = bottom - 45



# 开始游戏；从开始到进入战斗界面
def start_game(left, top, right, bottom):
  # 编成/出击
  flag = True
  click_right = right
  click_bottom = bottom
  while (flag):
    # 点击右下方
    click_team_start(click_right, click_bottom)
    screenshot = get_screenshot(left, top)
    global skill_pos_left
    global skill_pos_top
    # 检测skill1按钮是否存在
    if (is_has_tar_img(screenshot, 'skill1_normal')):
      # 存在则记录按钮位置
      skill_pos_left = left + global_pos[0]
      skill_pos_top = top + global_pos[1]
      flag = False
    else:
      # 如果没有进入战斗界面，则移动一点位置再点击
      click_right -= 1
      click_bottom -= 1

# 使用道具
def use_item():
  open_item_menu()
  mouse_move(item_pos_x, item_pos_y)
  mouse_click()
  mouse_move(item_use_pos_x, item_use_pos_y)
  mouse_click()
  
  

# 打开使用道具菜单
def open_item_menu():
  print("++ open item menu")
  # 打开之前先关闭
  # mouse_move(item_icon_pos_x, item_icon_pos_y - 70)
  # mouse_move(item_close_pos_x, item_close_pos_y)
  # mouse_click()
  click_item_button()

# 关闭使用道具菜单
def close_item_menu():
  print("-- close item menu")
  # mouse_move(item_icon_pos_x, item_icon_pos_y - 70)
  mouse_move(item_close_pos_x, item_close_pos_y)
  mouse_click()


# 点击item按钮
def click_item_button():
  mouse_move(item_icon_pos_x, item_icon_pos_y)
  print("item pos: ", item_icon_pos_x, item_icon_pos_y)
  mouse_click()




# 截取筹码图片
def shot_number_img(screenshot, pos_x, pos_y, width, height, out_file):
  img = Image.open(screenshot)
  region = (pos_x, pos_y, pos_x + width, pos_y + height)
  cropImg = img.crop(region)
  cropImg.save(f"{current_dir}/{out_file}")
  print("exported:", out_file)


# 处理图片提高识别率
def preprocess_image(image_path):
  # 1. 读取图像（保留原始色彩通道）
  img = cv2.imread(image_path, cv2.IMREAD_COLOR)

  # 2. 灰度化（非必须，根据场景选择）
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # 3. 噪声消除（自适应选择算法）
  denoised = cv2.fastNlMeansDenoising(
      gray, h=30) if np.mean(gray) < 200 else gray

  # 4. 二值化（动态阈值处理）
  thresh = cv2.adaptiveThreshold(
      denoised, 255,
      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
      cv2.THRESH_BINARY_INV, 11, 2
  )

  # 5. 形态学处理（强化文本）
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
  morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

  # 6. 边缘保留平滑
  smoothed = cv2.edgePreservingFilter(morph, flags=1, sigma_s=60, sigma_r=0.4)

  # 7. 对比度增强（CLAHE）
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
  enhanced = clahe.apply(smoothed)

  return enhanced




# 处理字符串，获取数字
def filter_text(ori_text):
  return re.sub(r'[^\d]', '', ori_text) 

# 获取n1数值
def get_num1():
  # 尝试次数
  repetitions = 0
  
  screenshot = f"{current_dir}/screenshot.png"
  num1_file_name = 'number1_img.png'
  size = 56
  num1_pos_x = 192
  num1_pos_y = 720 - 150 - size
  print("num1_pos_x: ", num1_pos_x)
  print("num1_pos_y: ", num1_pos_y)
  
  # 截取num1位置图片
  shot_number_img(screenshot, num1_pos_x, num1_pos_y, size, size, num1_file_name)
  # ocr获取n1数值
  # num_img = preprocess_image(f"{current_dir}/{num1_file_name}")
  
  config = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789"
  while(True):
    # 尝试不同方法识别
    if(repetitions % 2):
      num_img = Image.open(f"{current_dir}/{num1_file_name}")
    else:
      num_img = preprocess_image(f"{current_dir}/{num1_file_name}")
    
    num = pytesseract.image_to_string(num_img, 
                                          config=config)
    num = filter_text(num)
    print("num1 final: ==", num)
    
    if(num.isdigit()):
      return int(num)
    
    repetitions += 1
    # 重试次数超过5次则放弃识别
    if(repetitions > 3):
      return -1


# 处理num1的值
def handle_num1(num):
  print("handle num:  ", num)
  if(num == 21):
    # 攻击T位置
    open_skill1_menu()
    click_enemy_T()
    click_skill1_button()
  elif(num > 21 or num < 0):
    screenshot = get_screenshot(left, top)
    # 如果当前还有skill按钮，说明还在战斗界面中；因为数字识别不到/识别到错误值
    if(is_has_tar_img(screenshot, 'skill1_active') or is_has_tar_img(screenshot, 'skill1_normal') ):
      # 攻击A位置
      open_skill1_menu()
      click_enemy_A()
      click_skill1_button()
    else:
      keep_click_brc()
  elif(num < 18):
    # 攻击A位置
    open_skill1_menu()
    click_enemy_A()
    click_skill1_button()
  else:
    # 18-21之间，使用道具
    close_skill1_menu()
    print("use item")
    use_item()
  print("handle num: --------", num)


# 计算经过时间
def duration_time(start, end):
  return end - start


def main():
  global left
  global top
  global right
  global bottom
  
  # pyautogui.position()
  print(pyautogui.position())
  # 目标程序标题
  # title = "レスレリアーナのアトリエ"
  # # 获取目标窗口句柄
  # hwnd = win32gui.FindWindow(None, title)

  tar_window = get_tar_window()
  print(tar_window)
  pyautogui.PAUSE = 1
  if (tar_window):
    print(tar_window)
    left, top, right, bottom = win32gui.GetWindowRect(tar_window)
    # 将当前窗口的句柄激活（选中该窗口）
    win32gui.SetForegroundWindow(tar_window)
    # 获取目标窗口位置
    print(pyautogui.position(), left, top, right, bottom)
    left = left + 10
    top = top + 36
    
    # item按钮
    global item_icon_pos_x 
    global item_icon_pos_y 
    item_icon_pos_x += left
    item_icon_pos_y += top
    
    # item1物品位置
    global item_pos_x 
    global item_pos_y 
    item_pos_x = right - item_pos_x
    item_pos_y += top
    
    # action位置
    global item_use_pos_x 
    global item_use_pos_y 
    item_use_pos_x = right - item_use_pos_x
    item_use_pos_y = bottom -item_use_pos_y
    
    # 关闭菜单按钮位置
    global item_close_pos_x 
    global item_close_pos_y 
    item_close_pos_x = right - item_close_pos_x
    item_close_pos_y += top

    
    # time.sleep(1)
    # mouse_move(right - win_offset, bottom - win_offset)
    # mouse_click('double')

    # 截图时需要窗口在最上面，等待保证窗口已经是活动状态
    time.sleep(.5)

    
    start_game(left, top, right, bottom)
    
    
    while(True):
      print("---start loop")
      open_skill1_menu()      
      
      screenshot = get_screenshot(left, top)
      time.sleep(0.1)
      
      num1 = get_num1()
      
      handle_num1(num1)
      time.sleep(3)
      
      print("---loop")

          
      
          
      
      
      
    


if __name__ == '__main__':
  main()
