#!/usr/bin/env python
#coding:utf8
import os
import subprocess
 
def  getfiles(uuid):
    path = os.path.join("data", uuid)
    files = os.listdir(path)
    return files

def play(files)
    path = os.path.join("data", files)
    cmd = ["ffplay", path]
    subprocess

if __name__ == "__main__":
    print getfiles("123456123456")
    a = raw_input()
    print a ,type(a)
