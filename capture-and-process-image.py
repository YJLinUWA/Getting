# -*- coding: utf-8 -*-
import io, time, picamera, datetime, os
import numpy as np
from PIL import Image
import RPi.GPIO as GPIO

#Setup
path =os.getcwd()
frames =1

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(32,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(35,GPIO.IN,puLL_up_down=GPIO.PUD_DOWN) #trigger pin
red = GPIO.PWM(32,10000)
Ir = GPIO.PWM(33,10000)
camera = picamera.PiCamera()
camera.resolution = (480,640)
camera.framerate = 90


def capture():
    #capture.start = time.time()
    capture.count = 0
    try:
        while True:
            if GPIO.input(35)==GPIO.HIGH:
                camera.capture_sequence(['%03d-20Hz.jpg' %i for i in range(frames)],use_video_port=True)
                break
    finally:
        capture.stop = time.time()
        print('Captured %d frames at %.2ffps' %(frames, frames/(capture.stop-capture.start)))

def RGBtoGray(location):
    image = Image.open(location)
    rgb =np.array(image)
    r= rgb[:,:,0]
    g= rgb[:,:,1]
    b= rgb[:,:,2]
    array=0.2989*r+0.5870*g+ 0.1140*b
    array = array.astype(np.float32)
    array *= 1./255
    return array

def subtract():
    allfiles = os.Listdir(path)
    imlist =[filename for filename in allfiles if filename[-4:] in ['.jpg','.JPG']]
    listR =[item for index, item in enumerate(imlist) if index % 2== 0]
    listIR=[item for index, item in enumerate(imlist) if index % 2 !=0]
    arrayR =[RGBtoGray(item) for item in listR]
    arrayIR =[RGBtoGray(item) for item in listIR]
    subtract.stop_G = time.time()
    a = subtract.stop_G-substart
    arraySub =[np.subtract(arrayIR[index],arrayR[index]) for index, item in enumerate(arrayR)]
    array8bit =[((arraySub[index]-arraySub[index].min())*(1/(arraySub[index].max()-arraySub[index]
                                                             .min())*255)).astype('uint8')for index, item in enumerate(arraySub)]
    subtract.stop = time.time()
    b = subtract.stop-substart
    for index, item in enumerate(array8bit):
        image = Image.fromarray(array8bit[index])
        image.save('sub{}.jpg'.format(index))
        #image.show()
    return a,b;
camera.start_preview()
time.sleep(2)
substart = time.time()
if __name__=='__main__':
    t1 = time.time()
    capture()
    a,b=subtract()
    t2 = time.time()
    time.sleep(1)
    print('grayscaled %d frames at %.2ffps' % (frames, frames/a))
    print('subtracted %d frames at %.2ffps' % (frames, frames/b))
    print('whole process @ 2592x1952; %d frames at %.2ffps' % (4,4/(t2-t1)))

