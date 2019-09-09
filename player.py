#!/usr/bin/env python
#coding:utf8
import os
import time
import commands
 
def  getfiles(uuid):
    path = os.path.join("data", uuid)
    files = os.listdir(path)
    return files

def play(uuid, files):
    path = os.path.join("data", uuid, files)
    cmd = " ".join(["ffplay", path])
    start = time.time()
    commands.getstatusoutput(cmd)
    end = time.time()
    basename = os.path.basename(path)
    resourceid = os.path.splitext(basename)[0]
    return  int(resourceid), int(end - start)

if __name__ == "__main__":
    uuid = "123456123456"
    files = getfiles(uuid)
    print play(uuid, files[1])

    import time
    time.sleep(3)
