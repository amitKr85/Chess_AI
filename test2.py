# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 03:13:19 2019

@author: AMIT
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

def show_imgs(img_list, r, c, fig_num,size=(16,20), seprate=False, title_list=None, axis=True):
    if seprate:
        for i in range(len(img_list)):
            plt.figure(fig_num+i)
            plt.imshow(img_list[i],cmap='gray')
            if title_list is None:
                plt.title(i)
            else:
                plt.title(title_list[i])
            if not axis:
                plt.axis('off')
            plt.show()
        return
    
    plt.figure(fig_num,figsize=size)
    for i in range(r):
        for j in range(c):
            if i*c+j >= len(img_list):
                break
            plt.subplot(r,c,i*c+j+1)
            plt.imshow(img_list[i*c+j],cmap='gray')
#            plt.imshow(cv2.cvtColor(img_list[i*c+j],cv2.COLOR_BGR2RGB))
            if title_list is None:
                plt.title(i*c+j)
            else:
                plt.title(title_list[i*c+j])
    if not axis:
        plt.axis('off')
    plt.show()
    

def split_line(img):
    
    for i in range(1,8):
        cv2.line(img, (0,i*img.shape[0]*1//8),(img.shape[1],i*img.shape[0]*1//8),255,2)
        cv2.line(img, (i*img.shape[1]*1//8,0),(i*img.shape[0]*1//8,img.shape[0]),255,2)
        
# size must be tuple, size = size of each splitted pieces
def split_img(img,size=None):
    
    splitted_imgs = []
    if size and type(size)==tuple and len(size)==2:
        img = cv2.resize(img, (size[0]*8,size[1]*8))
    d0 = round(img.shape[0]*1/8)
    d1 = round(img.shape[1]*1/8)
    
    for i in range(8):
        for j in range(8):
            splitted_imgs.append(np.array(img[i*d0:(i+1)*d0,j*d1:(j+1)*d1],copy=True))
    return splitted_imgs

def get_train_data():
    imgs = [cv2.resize(cv2.imread('images/'+item,cv2.IMREAD_GRAYSCALE),(400,400)) for item in os.listdir('images/') if item.startswith('c_board_') ]
    """
    0 : Empty
    1 : Rook
    2 : Knight
    3 : Bishop
    4 : Queen
    5 : King
    6 : Pawn
    """
    tag = np.array([1,2,3,4,5,3,2,1,6,6,6,6,6,6,6,6,0,6,6,6,6,6,6,6,6,1,2,3,4,5,3,2,1])
    """
    0 : Black
    1 : White
    """
    tag = np.stack([tag, np.concatenate([np.zeros(16), np.ones(17)]) ],axis=1)
    
    X = []
    y = []
    for img in imgs:
        t = split_img(img)
        X.append(t[:16])
        X.append(t[-17:])
        y.append(np.array(tag,copy=True))
    
    X = np.concatenate(X)
    y = np.concatenate(y)
#    show_imgs(X[:64],8,8,0,title_list=y[:64])
    
    return X,y
        
#imgs = [cv2.imread('images/'+item,cv2.IMREAD_GRAYSCALE) for item in os.listdir('images/') if item.startswith('c_board_') ]
#show_imgs(imgs,2,3,0)
#
#li_imgs = [cv2.resize(np.array(img,copy=True),(400,400)) for img in imgs]
#
#for i in range(len(li_imgs)):
#    split_line(li_imgs[i])
#    
#show_imgs(li_imgs,2,3,11,seprate=True)
#
#sp_imgs = split_img(imgs[1])
#
#show_imgs(sp_imgs,8,8,2)