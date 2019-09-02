#!/usr/bin/env python
import paho.mqtt.client as mqtt
import json
import time
import threading
import hashlib
 
def on_message(client, userdata, msg):
    print "headset: %s topic: %s payload: %s"%(userdata.uuid, msg.topic, str(msg.payload))

def on_connect(client, userdata, flags, rc):
    print "headset: %s Connected: %s "%(userdata.uuid, str(rc))

class Headset(threading.Thread):

    #HOST = "mqtt.smartheadset.qctchina.top"
    HOST = "localhost"
    PORT = 1883


    def __init__(self, x):
        threading.Thread.__init__(self)
        self._mqtt = mqtt.Client(userdata=self)
        self._uuid =  "123456123456"
        self._sd = 4 #4GB
        self._level = 0 
        self._wifi = 1 
        self.playlist = list()
        self._x = x
        self.viewerfunc = None

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
            self.viewerfunc(self._x, "wifi","69","7GB","started", "blue")
        md5 = hashlib.md5()
        md5.update(self._uuid + "qtchina")
        password = md5.hexdigest()
        print password
        self._mqtt.username_pw_set(self._uuid, password)
        self._mqtt.on_connect = on_connect
        self._mqtt.on_message = on_message
        self._mqtt.connect(Headset.HOST, Headset.PORT, 60)
        self._mqtt.subscribe('/system/time',qos=2)
        self._mqtt.loop_start()
        while True:
           time.sleep(1)
           print "running headset"
           level = int(time.time()) % 100
           if self.viewerfunc != None:
               self.viewerfunc(self._x, "wifi",str(level),"7GB","connected", "blue")

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
