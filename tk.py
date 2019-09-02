#!/usr/bin/env python
#coding:utf8
import tkinter as tk

def print_hello():
    print "E"

class App():
   def __init__(self):
       self.main = tk.Tk()
       self.main.title("耳机模拟器")
       self.main.geometry('1080x720') 

   def create_menu(self):
       menubar = tk.Menu(self.main)
       fmenu = tk.Menu(menubar)
       for each in ['新建','退出']:
           fmenu.add_command(label=each, command=print_hello)
 
       amenu = tk.Menu(menubar)
       for each in ['版权信息','联系我们']:
           amenu.add_command(label=each, command=print_hello)
 
       menubar.add_cascade(label='文件',menu=fmenu)
       menubar.add_cascade(label='关于',menu=amenu)
 
       self.main.config(menu=menubar)

   def create_label(self):
       frame = tk.Frame(self.main)
       label = tk.Label(frame, width=40, text='序号',anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=40, text='设备序列号', anchor="center")	
       label.pack(side="left")
       label = tk.Label(frame, width=40, text='状态', anchor="center")	
       label.pack(side="left")
       frame.pack()

   def run(self):
       self.main.mainloop()

if __name__ =='__main__':
    app = App()
    app.create_menu()
    app.create_label()
    app.run()
