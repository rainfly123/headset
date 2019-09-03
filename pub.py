#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import hashlib
import time
 
HOST = "localhost"
PORT = 1883

mp31="http://resource.qctchina.top/NTBkMzJhOTMtYzkzMy0xMWU5LWE2NWYtZDQ2ZDZkOTYwNTdk.mp3"
mp32="http://resource.qctchina.top/NTg1NDBhODUtYzkzMy0xMWU5LWE2NWYtZDQ2ZDZkOTYwNTdk.mp3"

def aget():
    result = {"time":time.strftime("%Y_%m_%d-%H:%M:%S"),"Version":"1.0.0",
              "url":"http://a.b.c.d/a.bin"}
    return json.dumps(result)
 
def system_time():
    client = mqtt.Client()
    md5 = hashlib.md5()
    md5.update("123456123456"+ "qtchina")
    password = md5.hexdigest()
    print password
    client.username_pw_set("123456123456", password)
    client.connect(HOST, PORT, 60)
    client.publish("/system/time", bget(), 2) 
    client.loop_start()
    client.disconnect()

def bget():
 
    result1 = {"course_id": 23,
              "download_url":mp31,
              "resource_id":3000,
              "type":2}

    result2 = {"course_id": 23,
              "download_url":mp32,
              "resource_id":3001,
              "type":2}


    results = {"code":1, "data":[result1,result2]}
    return json.dumps(results)
    

def device_playlist(devid):
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    client.publish("/device/%s/playlist"%(devid), bget(), 2) 
    client.loop_start()
    client.disconnect()
 
if __name__ == '__main__':

    system_time()

    time.sleep(3)

   # device_playlist("0123456")
   # time.sleep(3)

