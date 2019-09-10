#!/usr/bin/env python
#coding:utf8
import os
import time
import commands
from client import send_message
 
def play(headset):
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

if __name__ == "__main__":
    uuid = "123456123456"
