# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:32:01 2019

@author: AMIT
"""
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os


def show_imgs(img_list, r, c, fig_num,size=(16,20),seprate=False):
    if seprate:
        for i in range(len(img_list)):
            plt.figure(fig_num+i)
            plt.imshow(img_list[i],cmap='gray')
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
            plt.title(i*c+j)
    plt.show()
    

def draw_lines(img ,lines):
    
    max_l = max(img.shape)
    print("max_l=",max_l)
    for line in lines:
        print(f"for line={line[0]}")
        rho,theta = line[0]
        # to remove lines that are not vertical/horizontal
        if theta != 0 and f'{theta:.2f}' != f'{(np.pi/2):.2f}':
            continue
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + max_l*(-b))
        y1 = int(y0 + max_l*(a))
        x2 = int(x0 - max_l*(-b))
        y2 = int(y0 - max_l*(a))
        print(f"{x1}:{y1},{x2}:{y2}")
        cv2.line(img,(x1,y1),(x2,y2),255,1)

def draw_linesP(img, lines):
    for line in lines:
        coords = line[0]
        if coords[0] - coords[2] == 0 or coords[1] - coords[3] == 0:
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), 255, 2)

def split_img(img):
    
    for i in range(1,8):
        cv2.line(img, (0,i*img.shape[0]*1//8),(img.shape[1],i*img.shape[0]*1//8),255,2)
        cv2.line(img, (i*img.shape[1]*1//8,0),(i*img.shape[0]*1//8,img.shape[0]),255,2)

        
        
imgs = [cv2.imread('images/'+item,cv2.IMREAD_GRAYSCALE) for item in os.listdir('images/') if item.startswith('c_board_') ]
show_imgs(imgs,2,3,0)
img = imgs[0]

plt.imshow(imgs[5],cmap='gray')

kernel = np.ones((3,3))*-1
kernel[1,1] = 8
kernel /= 9
edges = [cv2.filter2D(img, -1,kernel) for img in imgs]
for img in edges:
    img[img != 0]=255
#edgesc = [cv2.Canny(img,0,0) for img in imgs]
show_imgs(edges,2,3,2,seprate=True)
plt.figure(1)
plt.imshow(edges[0],cmap='gray')

lines = [cv2.HoughLines(edge,1,np.pi/180,round(max(edge.shape)*0.47)) for edge in edges]
#lines = [cv2.HoughLinesP(edge,1,np.pi/180,200,200,100) for edge in edges]
li_edges = [np.array(item,copy=True) for item in edges]

#draw_lines(li_edges[0],lines[0])
#plt.figure(2)
#plt.imshow(li_edges[0],cmap='gray')

for i in range(len(li_edges)):
    split_img(li_edges[i])
    
for i in range(len(lines)):
    if lines[i] is not None:
        draw_lines(li_edges[i],lines[i])

show_imgs(li_edges,2,3,11,seprate=True)

for i in range(len(imgs)):
    plt.figure(20+i)
    plt.subplot(131)
    plt.imshow(imgs[i],cmap='gray')
    plt.subplot(132)
    plt.imshow(edges[i],cmap='gray')
    plt.subplot(133)
    plt.imshow(li_edges[i],cmap='gray')
    
edges = cv2.blur(edges,(5,5))
cv2.imshow("blur edges",edges)
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,20,10)
draw_lines(li_edges,lines)
cv2.imshow("lines",li_edges)