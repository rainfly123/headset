#!/usr/bin/env python
#coding:utf8
import os
import time
import commands
from client import send_message
import tkinter
import tkinter.messagebox
import thread

def play(headset): 
    files = headset.todayplaylist
    if len(files) == 0:
        tkinter.messagebox.showwarning('警告','今天没有播放任务')
        return
    thread.start_new_thread(start_play, ("ffplay", headset))

def start_play(threadname, headset):
    uuid = headset.uuid
    files = headset.todayplaylist
    paths = [os.path.join("data", uuid, file) for file in files]
    for path in paths:
        cmd = " ".join(["ffplay", path])
        start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        commands.getstatusoutput(cmd)
        end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        basename = os.path.basename(path)
        resourceid = os.path.splitext(basename)[0]

        msg = {
        "businessCode": 807,
        "data": [{"headsetCourseResourceId":resourceid, "startTime":start,\
                        "endTime":end, "playProgress":100}]
        }
        send_message(headset, msg)
    tkinter.messagebox.showinfo('提示','今天任务已完成')

if __name__ == "__main__":
    uuid = "123456123456"
