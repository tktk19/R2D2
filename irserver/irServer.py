import cherrypy
import sys
import time
import serial
import json

class Root(object):

    def __init__(self):
        self.__ser = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)

    def index(self):
        return 'show'
    index.exposed = True


    def capture(self):
        self.__ser.open() 
        self.__ser.write("c\r\n")
        time.sleep(1.0)
        ret = self.__ser.readline()
        self.__ser.close()
        return ret
    capture.exposed = True


    def play(self):
        self.__ser.open()
        self.__ser.write("p\r\n")
        time.sleep(1.0)
        ret = self.__ser.readline()
        self.__ser.close()
        return ret
    play.exposed = True


    def load_and_play(self, target, action):
        filename = "/home/youk/iRData/" + target + "_" + action + ".json"
        f = open(filename)
        json_data = json.load(f)
        f.close()

        recNumber = len(json_data['data'])
        rawX = json_data['data']

        self.__ser.open()
        self.__ser.write("n,%d\r\n" % recNumber)

        time.sleep(1.0)

        postScale = json_data['postscale']
        self.__ser.write("k,%d\r\n" % postScale)
        self.__ser.readline()
 
        for n in range(recNumber):
            bank = n / 64
            pos = n % 64
            if (pos == 0):
                self.__ser.write("b,%d\r\n" % bank)
            
            self.__ser.write("w,%d,%d\n\r" % (pos, rawX[n]))
 
        self.__ser.write("p\r\n")
        ret = self.__ser.readline()
        self.__ser.close()
        
        return ret
    load_and_play.exposed = True

cherrypy.quickstart(Root())
