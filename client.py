#!/usr/bin/env python
#coding:utf8
import paho.mqtt.client as mqtt
import json
import time
import threading
import hashlib
import os
import urllib2

def  download(url, uuid):
    path = os.path.join("data", uuid)
    if os.path.exists(path) is False:
        os.mkdir(path)
    fileName = os.path.basename(url)
    writeFileName = os.path.join(path, fileName)
    if os.path.exists(writeFileName) is False:
        downloadFile = urllib2.urlopen(url)
        with open(writeFileName,'wb') as output:
            output.write(downloadFile.read()) 
        
    st = os.stat(writeFileName)
    return st.st_size
  
def OnLine(headset):
    msg = {
    "businessCode": 808,
    "data": {
        "batteryUsage": headset.level,
        "storageUsage": int(float(headset.total_download) / (headset.sd << 20) * 100),
        "location": "中国",
        "lastOnlineTime": time.strftime("%Y/%H/%d %H:%M:%S"),
        "network": headset.wifi
    }
    }
    return  json.dumps(msg)

def on_message(client, userdata, msg):
    print "headset: %s topic: %s payload: %s"%(userdata.uuid, msg.topic, str(msg.payload))
    temp = json.loads(msg.payload)
    userdata.playlists = temp['data']

def on_connect(client, userdata, flags, rc):
    print "headset: %s Connected: %s "%(userdata.uuid, str(rc))
    client.publish(Headset.Publish%(userdata.uuid), OnLine(userdata), 2)

class Headset(threading.Thread):

    HOST = "mqtt.smartheadset.qctchina.top"
    #HOST = "localhost"
    PORT = 1883
    Subscribe = "/hardware/from/server/%s"
    Publish = "/hardware/from/client/%s"


    def __init__(self, x):
        threading.Thread.__init__(self)
        self._mqtt = mqtt.Client(userdata=self)
        self._uuid =  "123456123456"
        self._sd = 4 #4GB
        self._level = 0 
        self._wifi = 1 
        self.playlists = list()
        self._x = x
        self.viewerfunc = None
        self.total_download = 0

    @property
    def uuid(self):
        return self._uuid
    @uuid.setter
    def uuid(self, val):
        self._uuid = val

    @property
    def sd(self):
        return self._sd
    @sd.setter
    def sd(self, val):
        self._sd = val

    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, val):
        self._level = val

    @property
    def wifi(self):
        return self._wifi
    @wifi.setter
    def wifi(self, val):
        self._wifi = val


    def run(self):
        if self.viewerfunc != None:
            self.viewerfunc(self._x, "wifi",self._level,self._sd,"started", "blue")
        md5 = hashlib.md5()
        md5.update(self._uuid + "qtchina")
        password = md5.hexdigest()
        print password
        self._mqtt.username_pw_set(self._uuid, password)
        self._mqtt.on_connect = on_connect
        self._mqtt.on_message = on_message
        self._mqtt.connect(Headset.HOST, Headset.PORT, 60)
        self._mqtt.subscribe(Headset.Subscribe%(self._uuid), qos=2)
        self._mqtt.loop_start()
        if self.viewerfunc != None:
            self.viewerfunc(self._x, "wifi",self._level,self._sd,"connected", "yellow")
        while True:
           time.sleep(3)
           print "{0}  wait for mqtt".format(self.uuid)
           for playlist in self.playlists:
               self.total_download += download(playlist['download_url'], self._uuid)
               if self.viewerfunc != None:
                  avaiable = self._sd - self.total_download/1024/1024/1024
                  self.level -= 1
                  self.viewerfunc(self._x, "wifi", self.level, avaiable, "downloading", "green")



    def viewer(self, func):
        self.viewerfunc = func


if __name__ == '__main__':
    d = Headset(1)
    d.uuid = "123456123456"
    d.wifi = 2
    d.level = 20
    d.sd = 8
    d.start()
    print d.uuid
    print d.level
    print d.wifi
    print d.sd
