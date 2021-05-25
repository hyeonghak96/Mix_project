# TCP client
#-*-coding: utf-8-*-
#-*-coding: euc-kr-*-
import sys
import os
import time
import picamera
import datetime

def imagefilesave():
    def fileName():
        dte = time.localtime()
        Year = dte.tm_year
        Mon = dte.tm_mon
        Day = dte.tm_mday
        WDay = dte.tm_wday
        Hour = dte.tm_hour
        Min = dte.tm_min
        Sec = dte.tm_sec
        imgFileName = str(Year) + '_' + str(Mon) + '_' + str(Day) + '_' + str(Hour) + '_' + str(Min) + '_' + str(
            Sec) + '.jpg'
        return imgFileName

    print("Start Camera App")
    # Server File Path
    src = "/home/pi/Desktop/"


    def transfer(filename):
        capture_file_name = "/home/pi/Desktop/picture/" + str(saveFileName) 

        # 3 Send File

        # Import img  (path/name)
        file = open(capture_file_name, "rb")
        img_size = os.path.getsize(capture_file_name)
        img = file.read(img_size)  # saved image
        file.close()

        print("Finish SendAll")

    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)
        camera.rotation = 0
        camera.framerate = 24
        camera.start_preview(fullscreen=False, window=(150,50,640,480))
        frame = 1
        # while True:
        saveFileName = fileName()
        camera.capture('/home/pi/Desktop/picture/' + saveFileName )
        fileName_list = [saveFileName]
        if saveFileName in fileName_list:
            transfer(saveFileName)
            time.sleep(3)
        frame += 1

    # print("App Stop")

    # camera.stop_preview()
    # camera.close()
