# ocr测试
import os
from PIL import Image
import pytesseract
import cv2
import numpy as np
import re


current_dir = os.path.dirname(os.path.abspath(__file__))
path = current_dir + "/example"

def shot_number_img(screenshot, pos_x, pos_y, width, height, out_file):
  img = Image.open(screenshot)
  region = (pos_x, pos_y, pos_x + width, pos_y + height)
  cropImg = img.crop(region)
  cropImg.save(f"{current_dir}/{out_file}")
  print("exported:", out_file)


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


def advanced_white_black_conversion(image_path):
    # 读取图像
  img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  
  # 降噪
  denoised = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
  
  # 自适应阈值
  binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 11, 2)
  
  # 形态学操作去除小噪点
  kernel = np.ones((2, 2), np.uint8)
  cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
  
  # 确保白底黑字
  if np.mean(cleaned) > 127:
      cleaned = cv2.bitwise_not(cleaned)
  
  return cleaned

# result = advanced_white_black_conversion('cut_res1.png')
# cv2.imwrite('advanced_white_black.png', result)


img = cv2.imread('number1_img.png', cv2.IMREAD_GRAYSCALE)

# 全局阈值二值化
_, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

# 确保是白底黑字（如果原图是黑底白字则反转）
if np.mean(binary) < 127:  # 如果图像大部分是白色
    binary = cv2.bitwise_not(binary)

cv2.imwrite('white_black_basic.png', binary)


# screenshot = f"{current_dir}/screenshot.png"
# print(screenshot)
# shot_number_img(screenshot, 193, 720-150 - 56, 56, 56, "cut_res1.png")
# # shot_number_img(screenshot, 651, 228, 82, 82, "cut_res2.png")


# num1_img = Image.open(f"{current_dir}/cut_res1.png")
# # num1_img = preprocess_image(f"{current_dir}/cut_res1.png")
# print(num1_img)
# # 需要添加config参数psm，否则无法识别出来
# num1 = pytesseract.image_to_string(num1_img,
#                                    config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789'")   # 识别图片
# print(num1)
# print(type(num1))

def extract_digits(text):
  """提取字符串中的所有数字"""
  return re.sub(r'[^\d]', '', text) 


num_img = Image.open(f"{current_dir}/white_black_basic.png")
# num_img = preprocess_image(f"{current_dir}/white_black_basic.png")
print(num_img)
# 需要添加config参数psm，否则无法识别出来
text = pytesseract.image_to_string(num_img,
                                  config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789")   # 识别图片
text = extract_digits(text)
# print("num1: ===", text)
# print(text.isdigit())
# print(int(text))


# shot_number_img(screenshot, 653, 230, 82, 82, "cut_res2.png")
# num_img = Image.open(f"{current_dir}/cut_res2.png")
# # num_img = preprocess_image(f"{current_dir}/cut_res2.png")
# print(num_img)
# # 需要添加config参数psm，否则无法识别出来
# text = pytesseract.image_to_string(num_img,
#                                   config="--psm 7")   # 识别图片
# # exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
# # text = ''.join([x for x in text if x not in exclude_char_list])
# print("num2: +++", text)
# print(int(text))


def image_to_position(screenshot, template):
  screen = cv2.imread(f"{screenshot}")
  image_x, image_y = template.shape[:2]
  result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
  print("prob:", max_val)
  if max_val > 0.95:
    # 中间位置
    pos = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
    return pos
  else:
    return (0, 0)


def is_has_tar_img(screenshot, template_name):
  template = cv2.imread(f"{path}/{template_name}.jpg")
  global global_pos
  global_pos = image_to_position(screenshot, template)
  print("========== ", global_pos)
  if (global_pos[0] != 0):
    return True
  return False

screenshot = f"{current_dir}/screenshot/network.jpg"
# is_has_tar_img(screenshot, 'next_btn')
print(is_has_tar_img(screenshot, 'net_tips'))
