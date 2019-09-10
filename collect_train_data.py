# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 13:07:43 2019

@author: AMIT
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from PIL import ImageGrab
import time
from image_processing import *
from key_check import key_check
import os



def process_image(img):
    res = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    res = retain_grayscale_BGR_old(res)
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    res = intensity_slice(res,40,120)
#    res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    res = intensity_slice(res, 40, 120)
    res = cv2.blur(res,(10,10))
    res = cv2.resize(res,(100,80))
    return res


def set_frame():
    print("set frame..")
    while True:
        test_img = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(5,30,800,625))), cv2.COLOR_RGB2BGR)
        cv2.imshow('window',test_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
#def process_image(img):
#    res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    res = intensity_slice(res, 50, 100, reverse=True)
#    res = cv2.blur(res,(10,10))
#    res = cv2.resize(res,(130,70))
#    return res

def keys_to_list(keys):
    input_keys = [0, 0, 0, 0] # W, A, S, D
    if 'W' in keys:
        input_keys[0] = 1
    if 'A' in keys:
        input_keys[1] = 1
    if 'S' in keys:
        input_keys[2] = 1
    if 'D' in keys:
        input_keys[3] = 1
    return input_keys

def main():
    set_frame()
    input("press enter to continue..")
    time.sleep(5)
    last_time = time.time()
    delay = []
    
#    file_name = 'training_data.npy'
#    if os.path.isfile(file_name):
#        print('File exists, loading previous data!')
#        data = list(np.load(file_name))
#    else:
#        print('File does not exist, starting fresh!')
    data = []
        
    flag = True
    while flag:
        last_time = time.time()
        printscreen =  np.array(ImageGrab.grab(bbox=(5,30,800,625)))
        printscreen = process_image(printscreen)
        cv2.imshow('window',printscreen)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            print(np.average(delay))
            break
        
        keys = key_check()
        input_keys = keys_to_list(keys)
        if 'Q' in keys:
            cv2.destroyAllWindows()
            print(np.average(delay))
            break
        
        data.append([printscreen,input_keys])
        
        delay.append(time.time()-last_time)
        print('loop took {} seconds keys={}'.format(delay[-1],keys))
        
    print("average loop time:",np.average(delay))
    np.save("training_data_100x80_willow_springs_rev_new",data)
    print("all done!!")

if __name__ == "__main__":
    main()