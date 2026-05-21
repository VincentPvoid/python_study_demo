import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


class GameInfoForm(ttk.Frame):
  def __init__(self, parent, on_get_info_callback, on_submit_callback):
    """
    初始化表单组件
    :param parent: 父容器
    :param on_get_info_callback: 点击获取游戏信息时触发，由调用组件的文件（模块）传入
    :param on_submit_callback: 点击提交时触发，由调用组件的文件（模块）传入
    """
    super().__init__(parent, padding="10")
    self.on_get_info_callback = on_get_info_callback
    self.on_submit_callback = on_submit_callback
    
    # 用字典存储所有复选框的变量，方便最后获取值
    self.checkbox_vars = {} 
    
    # 设置样式
    self.setup_styles()
    # 创建表单
    self.create_widgets()

    
  
  def setup_styles(self):
    """设置界面样式"""
    # self.root.configure(bg='#f0f0f0')

    # 字体样式
    self.title_font = ('微软雅黑', 14, 'bold')
    self.label_font = ('微软雅黑', 10)
    self.entry_font = ('微软雅黑', 10)
    self.button_font = ('微软雅黑', 10, 'bold')
  
  
  def create_widgets(self):
    """创建界面组件"""
    # 主框架
    self.main_frame = tk.Frame(self, bg='#f0f0f0', padx=10, pady=10)
    self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    # steam地址区域
    steam_frame = tk.LabelFrame(
        self.main_frame,
        text="steam url",
        font=self.label_font,
        bg='#f0f0f0',
        padx=15,
        pady=10
    )
    steam_frame.pack(fill=tk.X, pady=(0, 10))
  
    # URL 输入
    url_frame = tk.Frame(steam_frame, bg='#f0f0f0')
    url_frame.pack(fill=tk.X, pady=5)

    tk.Label(
        url_frame,
        text="steam url：",
        font=self.label_font,
        bg='#f0f0f0',
        width=10,
        anchor='e'
    ).pack(side=tk.LEFT, padx=(0, 10))
    
    # steam url输入框
    self.steam_url = tk.Text(
        url_frame,
        font=self.entry_font,
        width=50,
        relief='solid',
        borderwidth=1,
        height=1,
        undo=True
    )
    self.steam_url.pack(side=tk.LEFT, fill=tk.X, expand=True)
  
    # 发送请求按钮；发送请求获取游戏基本信息和封面
    self.get_info_btn = tk.Button(
        steam_frame,
        text="获取游戏信息",
        font=self.button_font,
        # bg='#2196F3',
        # fg='white',
        padx=5,
        pady=3,
        command=self.click_get_info
    )
    self.get_info_btn.pack(side=tk.LEFT, padx=5)
    
    
    # 一些信息回显
    req_info_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
    req_info_frame.pack(fill=tk.X, pady=(0, 15))
    self.req_info = scrolledtext.ScrolledText(
        req_info_frame,
        wrap=tk.WORD,
        font=('Consolas', 10),
        bg='#1e1e1e',
        fg='#d4d4d4',
        insertbackground='white',
        relief='solid',
        borderwidth=1,
        height=5
    )
    self.req_info.pack(fill=tk.X, expand=True)
        
    
    # 游戏信息表单填充区域
    info_frame = tk.LabelFrame(
        self.main_frame,
        text="游戏信息",
        font=self.label_font,
        bg='#f0f0f0',
        padx=15,
        pady=10
    )
    info_frame.pack(fill=tk.X, pady=(0, 10))
    
    # title
    tk.Label(
        info_frame,
        text="游戏标题：",
        font=self.label_font,
        bg='#f0f0f0',
        width=10,
        anchor='w'
    ).pack( padx=(0, 10))
    
    # 游戏标题
    self.game_title = tk.Text(
        info_frame,
        font=self.entry_font,
        width=50,
        relief='solid',
        borderwidth=1,
        undo=True,
        height=1
    )
    self.game_title.pack(fill=tk.X, expand=True)
    
    
    # infobox
    tk.Label(
        info_frame,
        text="游戏信息：",
        font=self.label_font,
        bg='#f0f0f0',
        width=10,
        anchor='w'
    ).pack(padx=(0, 10))
    
    # 游戏相关信息
    self.info_text = scrolledtext.ScrolledText(
        info_frame,
        wrap=tk.WORD,
        font=('Consolas', 12),
        bg='#fff',
        fg='#000',
        insertbackground='white',
        relief='solid',
        borderwidth=1,
        height=13
    )
    # 设置光标颜色
    self.info_text.configure(insertbackground='black', undo=True)
    self.info_text.pack(fill=tk.X, expand=True)
    self.info_text.insert(tk.END, "测试", 'info')
    
    
    # summary
    tk.Label(
        info_frame,
        text="游戏简介：",
        font=self.label_font,
        bg='#f0f0f0',
        width=10,
        anchor='w'
    ).pack(padx=(0, 10))
    
    # 游戏简介
    self.game_summary = scrolledtext.ScrolledText(
        info_frame,
        wrap=tk.WORD,
        font=('Consolas', 10),
        bg='#fff',
        fg='#000',
        insertbackground='white',
        relief='solid',
        borderwidth=1,
        height=5
    )
    # 设置光标颜色
    self.game_summary.configure(insertbackground='black')
    self.game_summary.pack(fill=tk.X, expand=True)
    # self.game_summary.insert(tk.END, "简介", 'info')
    
    
    # platform    
    tk.Label(
        info_frame,
        text="游戏平台：",
        font=self.label_font,
        bg='#f0f0f0',
        width=10,
        anchor='w'
    ).pack(padx=(0, 5))
  
    self._render_checkboxes(parent_container=info_frame)
    
    
    
    # 提交表单区域
    button_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
    button_frame.pack(fill=tk.X, pady=(0, 15))
    
    # 提交游戏信息按钮
    self.send_btn = tk.Button(
        button_frame,
        text="提交游戏信息",
        font=self.button_font,
        bg='#2196F3',
        fg='white',
        padx=30,
        pady=8,
        command=self.click_submit
    )
    self.send_btn.pack(side=tk.RIGHT, padx=5)
    
    
  # 渲染复选框区域
  def _render_checkboxes(self, parent_container):
    """
    专门负责渲染自动换行复选框的方法
    :param parent_container: 指定要装入的父级 Frame
    """
    platform_list_all = ["PC", "PS4", "PS5", "Nintendo Switch", "Xbox One", "Xbox Series X/S", "iOS", "Android"]
    
    # 创建一个普通的 Frame 作为内部网格容器
    grid_frame = tk.Frame(parent_container)
    grid_frame.pack(fill=tk.X, expand=True)
    
    MAX_COLS = 4
    
    for index, item in enumerate(platform_list_all):
      var = tk.BooleanVar()
      if(item == 'PC'):
        var.set(True)
      self.checkbox_vars[item] = var
       
      cb = tk.Checkbutton(
        grid_frame,
        text=item,
        variable=var,
        font=self.label_font,
        bg='#f0f0f0',
        # command=self.click_platform_checkbox
        command=lambda name=item: self.click_platform_checkbox(name)
      )
      
      row_num = index // MAX_COLS
      col_num = index % MAX_COLS
      
      cb.grid(row=row_num, column=col_num, sticky=tk.W, padx=3, pady=3)
      
    
  # 复选框点击事件，当点击取消勾选的值为最后一个时，禁止取消（保证至少要选择一个）
  def click_platform_checkbox(self, click_name):
    selected = [name for name, var in self.checkbox_vars.items() if var.get()]
    # print(selected)
    # print(self.checkbox_vars)
    if len(selected) == 0:
      self.checkbox_vars[click_name].set(True)
  
  
  
  # 点击获取游戏信息按钮
  def click_get_info(self):
    url = self.steam_url.get("1.0", tk.END).strip()
    
    if not url:
      # messagebox.showwarning("提示", "请输入请求地址！")
      self.req_info.delete("1.0", tk.END)
      self.req_info.insert(tk.END, "请输入请求地址", 'error')
      self.steam_url.focus()
      return
    
    if(self.on_get_info_callback):
      self.on_get_info_callback(url)
  
  
  # 提交信息表单验证
  def validate_form(self):
    title = self.game_title.get("1.0", tk.END).strip()
    infobox = self.info_text.get("1.0", tk.END).strip()
    summary = self.game_summary.get("1.0", tk.END).strip()
    
    if ((not title) or (not infobox) or (not summary)):
      return False
    return True
  
  # 点击提交游戏信息按钮   
  def click_submit(self):
    if not self.validate_form():
      return
    
    # 获取需要的数据
    data = {
      'title' : self.game_title.get("1.0", tk.END).strip(),
      'infobox': self.info_text.get("1.0", tk.END).strip(),
      'summary': self.game_summary.get("1.0", tk.END).strip(),
      'platform': [name for name, var in self.checkbox_vars.items() if var.get()]
    }
    print(data)
    print("===")
    
    if(self.on_submit_callback):
      self.on_submit_callback(data)
    
  
  def append_echo(self, text):
    """
    提供给外部调用的回显方法
    更新界面上的信息框
    """
    self.req_info.delete("1.0", tk.END)
    self.req_info.config(state='normal')
    self.req_info.insert(tk.END, text + "\n")
    self.req_info.see(tk.END)  # 自动滚动到最底部
    self.req_info.config(state='disabled')
    
  
  # 更新游戏信息区域
  def update_game_text_aera(self, text):
    self.info_text.delete("1.0", tk.END)
    self.info_text.insert(tk.END, text)
  
  # 更新游戏标题
  def update_game_title(self, title):
    self.game_title.delete("1.0", tk.END)
    self.game_title.insert(tk.END, title)
  
  # 修改get按钮状态
  def change_get_btn_status(self, status):
    self.get_info_btn.config(state=status)
  
  # 修改提交按钮状态
  def change_submit_btn_status(self, status):
    self.send_btn.config(state=status)