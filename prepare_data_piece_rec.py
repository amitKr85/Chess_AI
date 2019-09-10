# -*- coding: utf-8 -*-
"""
Created on Thu May 23 17:35:30 2019

@author: AMIT
"""
import numpy as np
import cv2
import os
from test2 import show_imgs, split_img

imgdata = []
tagdata = []

#path = 'dataset/chess-positions/test/'
path = 'images/test/'

for file in os.listdir(path):
#    file = "1b1B1b2-2pK2q1-4p1rB-7k-8-8-3B4-3rb3.jpeg"
    
    rows = file.split('.')[0].split('-')
    imgs = split_img(cv2.imread(path + file, cv2.IMREAD_GRAYSCALE), size=(50,50))
    
    #show_imgs(imgs[:10], 8,8, 0, seprate=True)
    blank = 0
    # parse positions
    p = {'R':1, 'N':2, 'B':3, 'Q':4, 'K':5, 'P':6}
    for i,row in enumerate(rows):
        j = 0
        for k in row:
            if k.isnumeric():
                j += int(k)
                if blank >= 0:
                    blank += int(k)
                    if blank >= 2:
                        imgdata.append(imgs[8*i+j-1])
                        tag = np.zeros(10)
                        tag[0] = tag[3] = 1
                        tagdata.append(tag)
                        blank = -1 # to not add more blank
                        
                    
            else:
                imgdata.append(imgs[8*i+j])
                tag = np.zeros(10)
                tag[1 + k.islower()] = 1 # assigning color [0] for none, [1] for white, [1] for black
                tag[3 + p[k.upper()]] = 1 # assigning piece val [3] for none, [4] for Rook and so on
                tagdata.append(tag)
                
                j += 1
                
imgdata = np.stack(imgdata)
tagdata = np.stack(tagdata)

show_imgs(imgdata[(tagdata[:,9]==1)&(tagdata[:,1]==1)][:64], 8,8, 0)
