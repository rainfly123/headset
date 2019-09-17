#!/usr/bin/env python
#coding:utf8
import paho.mqtt.client as mqtt
import json
import time
import threading
import hashlib
import os
import urllib2
import datetime

def isToday(timestamp):
    if timestamp >= 1568044800000:
        timestamp /= 1000
    input = datetime.date.fromtimestamp(timestamp)
    today = datetime.date.today()
    return input == today

def  download(url, uuid, resourceid):
    path = os.path.join("data", uuid)
    if os.path.exists(path) is False:
        os.mkdir(path)
    basename = os.path.basename(url)
    suffix = os.path.splitext(basename)[1]
    writeFileName = os.path.join(path, "{0}{1}".format(str(resourceid), suffix))
    if os.path.exists(writeFileName) is False:
        downloadFile = urllib2.urlopen(url)
        with open(writeFileName,'wb') as output:
            output.write(downloadFile.read()) 
        
        try:
            st = os.stat(writeFileName)
            return st.st_size
        except OSError:
            return 0
    return 0 

def deletefiles(uuid, resourceid_list):
    path = os.path.join("data", uuid)
    for resourceid in resourceid_list:
        file_name = os.path.join(path, resourceid)
        try:
            os.remove(file_name)
        except OSError:
            return -1
    return 0

def OnLine(headset):
    msg = {
    "businessCode": 808,
    "data": {
        "batteryUsage": headset.level,
        "storageUsage": int(float(headset.total_download) / (headset.sd << 30) * 100),
        "location": "中国",
        "lastOnlineTime": time.strftime("%Y-%H-%d %H:%M:%S"),
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

    elif businessCode == 809:
        data  = temp['data']
        if data['action'] == "delete":
            userdata.deletelists = data

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
        self._wifi = "wifi"
        self.playlists = list()
        self.todayplaylist = list()
        self._x = x
        self.viewerfunc = None
        self.total_download = 0
        self.connect_error  = False
        self.deletelists = dict()

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
           time.sleep(5)
           self._mqtt.publish(Headset.Publish%(self.uuid), OnLine(self), 2)
           if self.connect_error is True:
               self._mqtt.disconnect()
               break
           print "{0}  wait for mqtt".format(self.uuid)

           #report playlist
           msg = {"businessCode":803, "data":[]}
           for today in self.playlists:
               msg['data'].append({"headsetDownloadResourceId":today['headsetDownloadResourceId'],\
                                   "AckUpdateTime":today["updateTime"]})
           if len(msg['data']) > 0:
               send_message(self, msg)
           
           #report download
           dmsg = {"businessCode": 804, "data": []}
           for today in self.playlists:
               for playlist in today["playInfoList"]:
                   #get today's playlist
                   if today['playType'] == 1:
                       whichfile ="{0}.mp3".format(playlist['headsetCourseResourceId'])
                       if self.todayplaylist.count(whichfile) == 0:
                           self.todayplaylist.append(whichfile)
                   elif isToday(today['playTime']):
                       whichfile ="{0}.mp3".format(playlist['headsetCourseResourceId'])
                       if self.todayplaylist.count(whichfile) == 0:
                           self.todayplaylist.append(whichfile)

                   download_size = download(playlist['downloadUrl'], self.uuid,\
                                           playlist['headsetCourseResourceId'])
                   if download_size > 0 :
                      dmsg['data'].append(playlist['headsetCourseResourceId'])
                      self.total_download  += download_size
                      self.level -= 1
                      avaiable = self.sd - self.total_download/1024/1024/1024
                      if self.viewerfunc != None:
                          self.viewerfunc(self._x, "wifi", self.level, avaiable, "下载中", "green")

           if len(dmsg['data']) > 0:
               send_message(self, dmsg)
               print "\033[1;31;40m", dmsg
               print('\033[0m')

           if self.total_download > 0 and self.viewerfunc != None:
               self.viewerfunc(self._x, "wifi", self.level, avaiable, "全部完成", "green")

           print "\033[1;34;40m"
           print "#",self.todayplaylist
           print('\033[0m')
           #player.play(self)
           self.playlists = list()
           
           if self.deletelists.has_key('commandId'):
               val = deletefiles(self.uuid, self.deletelists['param'])
               if val == 0:
                   msg = {
                          "businessCode":809,
                          "data":{
                          "commandId":self.deletelists['commandId']}
                          }
                   send_message(self, msg)
                   self.deletelists = dict()



    def viewer(self, func):
        self.viewerfunc = func

def time_stamp(timestr):
    timesrt = time.strptime(timestr, "%Y-%m-%d")
    return time.mktime(timesrt)

def getFilesCreateTime(uuid):
    mydir = os.path.join("data/%s"%(uuid))
    for root, dirs, files in os.walk(mydir, topdown=False):
        for name in files:
            checkfile = os.path.join(mydir, name)
            st = os.stat(checkfile)
            return int(st.st_mtime)

if __name__ == '__main__':
    getFilesCreateTime("123456123456")
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
