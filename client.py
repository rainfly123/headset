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
    return 0 

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

def send_message(headset, msg):
    data = json.dumps(msg)
    headset._mqtt.publish(Headset.Publish%(headset.uuid), data, 2) 

def on_message(client, userdata, msg):
    print "headset: %s topic: %s"%(userdata.uuid, msg.topic)
    temp = json.loads(msg.payload)
    businessCode = temp['businessCode']
    if businessCode == 802:
        data  = temp['data']
        userdata.playlists = data

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print "headset: %s Connected "%(userdata.uuid)
        client.publish(Headset.Publish%(userdata.uuid), OnLine(userdata), 2)
        client.subscribe(Headset.Subscribe%(userdata.uuid), qos=2)
    else:
        userdata.connect_error = True
        if userdata.viewerfunc != None:
            userdata.viewerfunc(userdata._x, "wifi", userdata.level, userdata.sd, "连接错误", "red")

class Headset(threading.Thread):

    HOST = "mqtt.smartheadset.qctchina.top"
    #HOST = "localhost"
    PORT = 1883
    Subscribe = "hardware/from/server/%s"
    Publish = "hardware/from/client/%s"


    def __init__(self, x):
        threading.Thread.__init__(self)
        self._uuid =  "123456123456"
        self._sd = 4 #4GB
        self._level = 0 
        self._wifi = 1 
        self.playlists = list()
        self._x = x
        self.viewerfunc = None
        self.total_download = 0
        self.connect_error  = False

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

    def __getPassword(self):
        md5 = hashlib.md5()
        md5.update(self.uuid + "qctchina")
        password = md5.hexdigest()
        return password

    def run(self):
        if self.viewerfunc != None:
            self.viewerfunc(self._x, "wifi",self._level,self._sd,"started", "blue")

        self._mqtt = mqtt.Client(client_id = self.uuid, userdata=self)
        password = self.__getPassword()
        print password
        self._mqtt.username_pw_set(self.uuid, password)
        self._mqtt.on_connect = on_connect
        self._mqtt.on_message = on_message
        self._mqtt.connect(Headset.HOST, Headset.PORT, 60)
        self._mqtt.loop_start()
        if self.viewerfunc != None:
            self.viewerfunc(self._x, "wifi",self.level,self.sd,"已连接", "yellow")
        while True:
           time.sleep(3)
           if self.connect_error is True:
               self._mqtt.disconnect()
               break
           print "{0}  wait for mqtt".format(self.uuid)
           msg = {"businessCode":803, "data":[]}
           for today in self.playlists:
               msg['data'].append({"headsetDownloadResourceId":today['headsetDownloadResourceId'],\
                                   "AckUpdateTime":today["updateTime"]})
           send_message(self, msg)

           for today in self.playlists:
               for playlist in today["playInfoList"]:
                   download_size = download(playlist['downloadUrl'], self.uuid)
                   if download_size > 0 and self.viewerfunc != None:
                      self.total_download  += download_size
                      avaiable = self.sd - self.total_download/1024/1024/1024
                      self.viewerfunc(self._x, "wifi", self.level, avaiable, "下载中", "green")


           if self.total_download > 0:
               self.viewerfunc(self._x, "wifi", self.level, avaiable, "全部完成", "green")
           self.level -= 1



    def viewer(self, func):
        self.viewerfunc = func


if __name__ == '__main__':
    d = Headset(1)
    d.uuid = "123456123456"
    d.wifi = "4G"
    d.level = 20
    d.sd = 8
    d.start()
    print d.uuid
    print d.level
    print d.wifi
    print d.sd
