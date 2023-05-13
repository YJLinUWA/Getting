# -*- coding: utf-8 -*-
"""
Created on Sat May 13 17:04:03 2023

@author: HUAWEI
"""

import io, time, picamera, datetime, os
import numpy as np
from PIL import Image
import RPi.GPIO as GPIO

#Setup
path =os.getcwd()
frames =1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

camera = picamera.PiCamera()

imageRed = Image.open(location)
rgb =np.array(imageRed)
r= rgb[:,:,0]
g= rgb[:,:,1]
b= rgb[:,:,2]
arrayRed=0.2989*r+0.5870*g+ 0.1140*b
arrayRed = arrayRed.astype(np.float32)
arrayRed *= 1./255

imageInfrared = Image.open(location)
rgb =np.array(imageInfrared)
r= rgb[:,:,0]
g= rgb[:,:,1]
b= rgb[:,:,2]
arrayInfrared=0.2989*r+0.5870*g+ 0.1140*b
arrayInfrared = arrayInfrared.astype(np.float32)
arrayInfrared *= 1./255

arraySub =[np.subtract(arrayInfrared,arrayRed)]
array8bit =[((arraySub-arraySub.min())*(1/(arraySub.max()-arraySub.min())*255)).astype('uint8')]

image = Image.fromarray(array8bit)
image.save('sub{}.jpg')
image.show()