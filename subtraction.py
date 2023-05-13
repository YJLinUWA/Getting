# -*- coding: utf-8 -*-
"""
Created on Sat May 13 17:04:03 2023

@author: HUAWEI
"""

import io, time, picamera, datetime, os
import numpy as np
from PIL import Image
import RPi.GPIO as GPIO

camera = picamera.PiCamera()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


camera.start_preview()
GPIO.setup(14,GPIO.OUT)
print("LED on")
GPIO.output(14,GPIO.HIGH)
time.sleep(1)
camera.capture('/home/yijunlin/Desktop/image3.jpg')
time.sleep(1)
print("LED off")
GPIO.output(14,GPIO.LOW)

GPIO.setup(15,GPIO.OUT)
print ("LED on")
GPIO.output(15,GPIO.HIGH)
time.sleep(1)
camera.capture('/home/yijunlin/Desktop/image4.jpg')
time.sleep(1)
print ("LED off")
GPIO.output(15,GPIO.LOW)

camera.stop_preview()

imageRed = Image.open('/home/yijunlin/Desktop/image3.jpg')
rgb =np.array(imageRed)
r= rgb[:,:,0]
g= rgb[:,:,1]
b= rgb[:,:,2]
arrayRed=0.2989*r+0.5870*g+ 0.1140*b
arrayRed = arrayRed.astype(np.float32)
arrayRed *= 1./255

imageInfrared = Image.open('/home/yijunlin/Desktop/image4.jpg')
rgb =np.array(imageInfrared)
r= rgb[:,:,0]
g= rgb[:,:,1]
b= rgb[:,:,2]
arrayInfrared=0.2989*r+0.5870*g+ 0.1140*b
arrayInfrared = arrayInfrared.astype(np.float32)
arrayInfrared *= 1./255

arraySub =[np.subtract(arrayInfrared[index],arrayRed[index]) for index, item in enumerate(arrayRed)]
array8bit =[((arraySub[index]-arraySub[index].min())*(1/(arraySub[index].max()-arraySub[index].min())*255)).astype('uint8')for index, item in enumerate(arraySub)]

image = Image.fromarray(array8bit[0])
image.save('/home/yijunlin/Desktop/sub.jpg')
image.show()