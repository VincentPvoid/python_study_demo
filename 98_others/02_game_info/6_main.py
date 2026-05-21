import tkinter as tk
import requests
from bs4 import BeautifulSoup
from dateutil import parser
import re
import concurrent.futures
import time
import json
import threading

from formView import GameInfoForm
import util as ut


# 请求常量（主要用于提交信息）
FORM_BASE_URL = 'https://bgm.tv/new_subject/4'
BGM_HEADERS = {
      'Cookie':"user cookie",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }
DEFAULT_PROXY = {'https': 'http://127.0.0.1:7890', 'http': 'http://127.0.0.1:7890'}



class MainApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Game Info")
    self.root.geometry("600x900")
    self.root.resizable(True, True)

    # 实例化的表单组件，并将自己的 handle_form_submit 方法传给它
    self.form_view = GameInfoForm(
        self.root, on_get_info_callback=self.handle_get_info, on_submit_callback=self.handle_submit_form)
    self.form_view.pack(fill="both", expand=True)

  
  
  # 处理steam商店页面响应，获取后半段字符串
  def handle_main_url(res, url):
    content = res.text
    soup = BeautifulSoup(content, 'lxml')
  
    # 日期；如果未定获取到的字符串为To be announced 或 Coming soon
    date = soup.select('.date')[0].get_text()
    # print(date)
    try:
      date = ut.format_date(date)
    except:
      date = "未定"
    # print(title, description, date)
    developers_a_list = soup.select('#developers_list a')
    publishers_a_list = soup.select('.dev_row .summary a')
    tags_list = soup.select('.popular_tags a')
    try:
      link = soup.select('.details_block .linkbar')[0].attrs['href'].replace('%2F','/').replace('%3A', ':')
    except:
      link = ""
    # print(link)
    
    
    # 获取图片地址，并去除后面的时间参数 ?=xxxxxx 部分，方便后面正则过滤
    img_src = soup.select('.game_header_image_full')[0].attrs['src'].split('?')[0]
    
    # 去除数字到header之前的部分
    img_src = re.sub(r'/(\d+)/[^/]+(/header[^/]+)', r'/\1\2', img_src)
    if(img_src):
      # 替换header，获取竖图地址
      img_src = re.sub(r'(/header)[^/.]*\.', r'/library_600x900.', img_src)
    print(img_src)
    ut.dl_img(img_src)
    
    developers = ut.get_dev_str(developers_a_list)
    publishers = ''
    tags = ut.get_tags_str(tags_list)
    
    # 发行商字符串
    for i in range(len(developers_a_list), len(publishers_a_list)):
      publishers += publishers_a_list[i].get_text()
      if(i != len(publishers_a_list) - 1):
        publishers += ','
        
    text2 = f"""
|游戏类型= {tags}
|游戏引擎= 
|游玩人数= 1
|发行日期= {date}
|售价= $
|开发= {developers}
|发行= {publishers}
|website= {link}
|链接={{
[Steam|{url}]
"""
    return text2
  
  
  # 处理steamcmd响应，获取前半段字符串和竖向大图
  def handle_steamcmd_url(res, app_id):
    # res.encoding = 'utf-8'
    
    # 把字符串转换为json，方便获取对应值
    res_json = json.loads(res.text)
    # 竖图地址
    img_src = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{app_id}/" + res_json['data'][app_id]['common']['library_assets_full']['library_capsule']['image']['english']
    print(img_src)
    ut.dl_img(img_src, 'header2.jpg')
    
    # 游戏标题
    game_title = res_json['data'][app_id]['common']['name']
    
    # 需要的语种标题列表
    tar_list = [{'tchinese':'繁中'}, {'japanese':'日文'}, {'koreana':'韩文'}]
    try:
      # 获取到的不同语种标题
      title_obj = res_json['data'][app_id]['common']['name_localized']
      # 获取当前有的标题字段
      title_text_part = f'{{{ut.build_string_from_dict(title_obj, tar_list)}}}'
      ch_title = title_obj.get('schinese', '')
    except:
      title_text_part = ''
      ch_title = ''
    
    platforms = ["PC"]
    # 将列表转为换行分隔的字符串
    platforms_str = "\n".join(f"[{p}]" for p in platforms)
      
    text1 = f"""{{{{Infobox Game
|中文名= {ch_title}
|别名= {title_text_part}
"""
    obj = {
      "text" : text1,
      "game_title" : game_title
    }
    # return text1
    return obj
  
  
  # 请求并处理响应
  def fetch_url(url):
    # proxy = {'https': 'http://127.0.0.1:7890', 'http': 'http://127.0.0.1:7890'}
    try:
      response = requests.get(url=url, proxies=DEFAULT_PROXY)
      # 如果请求失败，抛出HTTPError异常
      response.raise_for_status()  
      # 返回响应内容
      # return response
      
      # 因为后面还需要用到url，所以把url和结果都存入到一个对象中，再返回
      obj = {
        "url": url,
        "res": response
      }
      return obj
    except requests.RequestException as e:
      print(f"Error fetching {url}: {e}")
      return None
  
  # 自定义生成器，添加请求间隔
  def url_generator(url_list, interval):
    for url in url_list:
      yield url
      print(url)
      # 设置请求间隔
      time.sleep(interval)
      
  # 使用ThreadPoolExecutor并发发送请求  
  def fetch_all_urls(url_list):  
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:  
      # 使用executor.map来自动处理迭代和Future的获取  
      # results = executor.map(fetch_url, url_list) 
       
      results = executor.map(MainApp.fetch_url, MainApp.url_generator(url_list, 0))  
    # print(results)
    return results
  
  
  # 从steam中获取游戏信息和图片（并发）
  def get_game_info(self, url):
    
    try:
      # 替换获取steamcmd请求地址
      steamcmd_url = re.sub('store.steampowered.com/app', 'api.steamcmd.net/v1/info', url)
      
      # 获取steam应用id
      app_id = url.rstrip("/").split("/")[-1] 
      
      # url对应处理函数map
      url_handler_map = {
        url: MainApp.handle_main_url,
        steamcmd_url: MainApp.handle_steamcmd_url
      }
      
      url_list = [steamcmd_url, url]
      res_list = MainApp.fetch_all_urls(url_list)
      
      main_text = ''
      for item in res_list:
        if item is not None:
          # print(item.get('url'), item.get('res').text)
          # steam 请求响应
          if item.get('url') == url:
            text2 = url_handler_map[url](item.get('res'), url)
          else:
            # steamcmd 请求响应
            steamcmd_obj = url_handler_map[steamcmd_url](item.get('res'), app_id)
            text1 = steamcmd_obj['text']         
      
      main_text = text1 + text2
      # 去除多余空行
      main_text = re.sub(r'\n{2,}', '\n', main_text.strip())
      # 添加结尾
      main_text += '\n}\n}}'
      # print(text1 + text2)
      
      # 完成后信息显示到表单中
      self.form_view.after(0, self.form_view.update_game_text_aera, main_text)
      self.form_view.append_echo('请求完成')
      self.form_view.update_game_title(steamcmd_obj['game_title'])
      # self.form_view.change_get_btn_status('normal')
    except Exception as e:
      print(e)
      # self.form_view.change_get_btn_status('normal')
    finally:
      self.form_view.change_get_btn_status('normal')
      
    
    # 保存字符串为文本文件
    def save_txt(file_name, file_content):
      with open(file_name.replace('/', '_') + ".txt", "w", encoding='utf-8') as f:
        f.write(file_content)
  
    save_txt('test', main_text)
  
  
  # 点击按钮，获取游戏信息
  def handle_get_info(self, url):
    self.form_view.append_echo(f"开始发送请求 {url} ")
    self.form_view.update_game_text_aera('请求中，请勿填充此处')
    self.form_view.change_get_btn_status('disabled')
    
    thread = threading.Thread(
        target=self.get_game_info,
        args=(url,),
        daemon=True
    )
    thread.start()
    
  
  
  # 信息提交完成后，上传封面图片
  def upload_game_img(subject_url):
    upload_img_url = subject_url + '/upload_img'
    data = {
      'formhash': '1ed8bc3f',
      'submit': '上传图片'
    }
    files = {
      'picfile': open('header2.jpg', 'rb')
    }
    
    response = requests.post(url=upload_img_url, proxies=DEFAULT_PROXY, headers=BGM_HEADERS, data=data, files=files)
    if (response.status_code == 200):
      print("图片上传完成")
    else:
      print("图片上传失败")
  
  
  
  # 提交游戏信息表单
  def submit_form(self, form_data):
    # url = 'https://bgm.tv/new_subject/4'
    # print(form_data)
        
    # 获取当前所选平台
    platforms_arr = form_data['platform']
    insert_text = f"""|平台= {{
{"\n".join(f"[{platform}]" for platform in platforms_arr)}
}}""" 
    # 在infobox中插入平台字符串（在游戏类型的上一行插入）
    search_text = "|游戏类型="
    game_infobox = ut.search_insert_text(form_data['infobox'], search_text, insert_text)
    
    data = {
      'formhash': '1ed8bc3f',
      'subject_title': form_data['title'],
      'platform': '4001',
      # 'subject_infobox' : form_data['infobox'],
      'subject_infobox' : game_infobox,
      'subject_summary': form_data['summary'],
      'submit': '提交'
    }
    print(data)
    # print(self.upload_game_img)
    
    # 注意需要设定 allow_redirects=False ，才能获取到响应头中的Location
    response = requests.post(url=FORM_BASE_URL, proxies=DEFAULT_PROXY, headers=BGM_HEADERS, data=data, allow_redirects=False)
    new_url = 'https://bgm.tv/' + response.headers['Location']
    # 上传图片
    MainApp.upload_game_img(new_url)
    print(response.headers)
    
    self.form_view.after(0, self.form_view.append_echo, "提交完成")
    self.form_view.change_submit_btn_status('normal')
    
    
    
  # 点击按钮，提交游戏信息
  def handle_submit_form(self, data):
    self.form_view.append_echo(f"提交游戏信息中... ")
    # 改变提交按钮状态为禁止状态
    self.form_view.change_submit_btn_status('disabled')
    
    thread = threading.Thread(
        target=self.submit_form,
        args=(data,),
        daemon=True
    )
    thread.start()
  
  
    
  
  
  
  
  


if __name__ == "__main__":
  # 创建主窗口
  root = tk.Tk()

  # 启动应用
  app = MainApp(root)

  # 运行主循环
  root.mainloop()
