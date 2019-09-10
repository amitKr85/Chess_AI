# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:26:47 2019

@author: AMIT
"""
import pickle
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from test2 import show_imgs,split_img

with open("classifier_piece_color.pickle","rb") as fil:
    color_classifier = pickle.load(fil)
with open("classifier_piece.pickle","rb") as fil:
    piece_classifier = pickle.load(fil)

# new classifier
with open("lichess_classifier.pickle","rb") as file:
    classifier = pickle.load(file)

"""
team=0 : black
team=1 : white
"""
def analyse_board(img,team=1):
    img = cv2.resize(img, (400,400))
    splitted_imgs = np.stack(split_img(img),axis=0)
    splitted_imgs = splitted_imgs.reshape((splitted_imgs.shape[0],splitted_imgs.shape[1],splitted_imgs.shape[2],1))
    
    piece_tag = np.array(['','R','N','B','Q','K','P'])
    positions = []
#    return splitted_imgs, color_classifier.predict(splitted_imgs), piece_classifier.predict(splitted_imgs)
    # for old classifiers
#    cols = color_classifier.predict(splitted_imgs)
#    pieces = piece_classifier.predict(splitted_imgs)
#    cols = np.where(cols>=0.5,1,0)[:,0]
#    pieces = np.argmax(pieces,axis=1)
    
    # for new all in one classifiers
    y_pred = classifier.predict(splitted_imgs)
    cols = np.argmax(y_pred[0], axis=1)
    pieces = np.argmax(y_pred[1], axis=1)
    
    for i in range(len(pieces)):
        pos = ''
        # old
#        pos += 'B' if cols[i] == 0 else 'W'
        # new
        pos += 'B' if cols[i] == 2 else 'W'
        pos += piece_tag[pieces[i]]
        if team == 1:
            pos += chr(65+i%8)
            pos += str(8-(i//8))
        else:
            pos += chr(72-i%8)
            pos += str((i//8)+1)
        if pieces[i] != 0:
            positions.append(pos)
        else:
            positions.append('')
#        col = color_classifier.predict([img])
#        ps = piece_classifier.predict([])
    return splitted_imgs, positions

path = 'images/test/'

for i,file in enumerate(os.listdir(path)[:5]):
    img = cv2.imread(path+file, cv2.IMREAD_GRAYSCALE)
    plt.figure(i)
    plt.imshow(img,cmap='gray')
    plt.show()
    splitted_imgs, positions = analyse_board(img,team=1)
    show_imgs(splitted_imgs.reshape((64,50,50)),8,8,100+i,title_list=positions,axis=False)
    
    
img = cv2.imread('images/c_board_1.jpg',cv2.IMREAD_GRAYSCALE)
plt.imshow(img,cmap='gray')


#splitted_imgs, y_c_pred, y_p_pred = analyse_board(img)
splitted_imgs, positions = analyse_board(img,team=1)
#y_p_pred = np.argmax(y_p_pred,axis=1)
#y_c_pred[y_c_pred>=0.5]=1
#y_c_pred[y_c_pred<0.5]=0
#piece = np.array(['','R','K','B','Q','K','P'])
show_imgs(splitted_imgs.reshape((64,50,50)),8,8,0,title_list=positions)