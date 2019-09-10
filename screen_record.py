# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:49:25 2019

@author: AMIT
"""

import numpy as np
from PIL import ImageGrab
import cv2
import time
from image_processing import *


def draw_lines(img, lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)


def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, (255,255,255))
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_image(img):
    res = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#    res = intensity_slice(res, 40, 120, reverse=True)
#    res = cv2.blur(res,(10,10))
#    res = cv2.Canny(res, 100, 150)
#    vertices = np.array([[0,600],[0,200],[200,150],[600,150],[800,200],[800,600],[750,600],[400,500],[50,600]], np.int32)
#    res = roi(res, [vertices])
#    res = cv2.GaussianBlur(res, (5,5), 0)
#    # img, p, 0, minVote, minLength, maxGap
#    lines = cv2.HoughLinesP(res, 1, np.pi/180, 180, 20, 15)
#    draw_lines(res, lines)
#    
#    res = cv2.resize(res,(400,310))
    return res


def process_image_old(img):
    res = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    res = intensity_slice(res, 40, 120)
    res = cv2.blur(res,(10,10))
    res = cv2.resize(res,(400,300))
    return res

def process_image_new(img):
    res = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    res = retain_grayscale_BGR(res)
    res = intensity_slice_BGR(res,(40,120),(40,120),(40,120))
    
#    vertices = np.array([[0,600],[0,200],[800,200],[800,600]],np.int32)
#    res = roi(res, [vertices])
    res = cv2.blur(res,(10,10))
#    res = intensity_slice_RGB(res, (40,120),(40,120),(40,120), reverse=True)
#    res = cv2.blur(res,(10,10))
    res = cv2.resize(res,(400,300))
    return res

def process_image_new2(img):
    res = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    res = retain_grayscale_BGR_old(res)
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    res = intensity_slice(res,40,120)
    res = cv2.blur(res,(10,10))
#    res = intensity_slice_RGB(res, (40,120),(40,120),(40,120), reverse=True)
#    res = cv2.blur(res,(10,10))
    res = cv2.resize(res,(400,300))
    return res

def screen_record(): 
    
#    cv2.imshow('intensity_slice',cv2.resize(cv2.imread("test.jpg",cv2.IMREAD_GRAYSCALE),(400,310)))
#    cv2.imshow('hpf',cv2.resize(cv2.imread("test.jpg",cv2.IMREAD_GRAYSCALE),(795,595)))
    
    save_data = False
    if save_data:
        time.sleep(5)
    last_time = time.time()
    delay = []
    
    data = []
    while(True):
        last_time = time.time()
        # (5,30,1280,625) for 1280x600 windowed mode
        # (5,30,1280,745) for 1280x720 windowed mode
        printscreen =  np.array(ImageGrab.grab(bbox=(5,30,800,625)))
#        printscreen = printscreen[:,:540,:]
        #printscreen = cv2.resize(printscreen,(1,25))
#        printscreen = cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY)
        img_old = process_image_new(printscreen)
        img_new = process_image_new2(printscreen)
#        img_hpf = process_hpf(printscreen)
        
        cv2.imshow('old',img_old)
        cv2.imshow('new',img_new)
#        cv2.imshow('hpf',img_hpf)
        
        if save_data:
            data.append(img)
            time.sleep(2)
            
        delay.append(time.time()-last_time)
        print('loop took {} seconds'.format(delay[-1]))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            print(np.average(delay))
            break
    if save_data:
        np.save("temp_screen_data",data)
        
#screen_record()

"""img_data = np.load("img_data.npy")
for i in range(len(img_data)):
    cv2.imshow('window',img_data[i])
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
"""