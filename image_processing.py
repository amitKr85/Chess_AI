# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:43:07 2019

@author: AMIT
"""
import numpy as np

def contrast_strech_gray(imgs,r1,r2,s1,s2):
    alpha = s1/r1
    beta = (s2-s1)/(r2-r1)
    gamma = (255-s2)/(255-r2)
    
    res = np.array(imgs, copy=True)
    for k,img in enumerate(imgs):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j] < r1:
                    res[k][i][j] = alpha*img[i][j]
                elif img[i][j] < r2:
                    res[k][i][j] = beta*(img[i][j] - r1) + s1
                else:
                    res[k][i][j] = gamma*(img[i][j] - r2) + s2
    return res

def intensity_slice(imgs,r1,r2,reverse=False):
    res = np.array(imgs, copy=True)
    res[imgs < r1] = 255 if reverse else 0
    res[imgs > r2] = 255 if reverse else 0
    res[res != (255 if reverse else 0)] = 0 if reverse else 255
    return res

def intensity_slice_BGR(img, br, gr, rr, reverse=False):
    #res = np.array(imgs, copy=True)
    b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
    r = intensity_slice(r,rr[0],rr[1])
    g = intensity_slice(g,gr[0],gr[1])
    b = intensity_slice(b,br[0],br[1])
    
    sel_pixels = np.logical_and(r, np.logical_and(g, b))
    tres = np.stack([b*sel_pixels, g*sel_pixels, r*sel_pixels],axis=2)
    if reverse:
        res = np.array(tres,copy=True)
        res[tres==255] = 0
        res[tres==0] = 255
        return res
    else:
        return tres
    #res = res*sel_pixels
    
def selective_highlight(imgs,r1,r2, reverse=False):
    res = np.array(imgs, copy=True)
    res[np.bitwise_and(imgs>=r1,imgs<=r2)] = 0 if reverse else 255
    return res
        

def retain_grayscale_BGR_old(img):
    
    b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
    
    lim = 20
    r_g_diff = np.abs(r-g)<lim
    g_b_diff = np.abs(g-b)<lim
    r_b_diff = np.abs(r-b)<lim
    
    mask = r_g_diff & g_b_diff & r_b_diff
    
    r = r*mask
    g = g*mask
    b = b*mask
    
    return np.stack([b,g,r],axis=2)


def retain_grayscale_BGR(img):
    
    img = np.array(img,copy=True,dtype='int')
    b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
    
    lim = 20
    r_g_diff = np.abs(r-g)<lim
    g_b_diff = np.abs(g-b)<lim
    r_b_diff = np.abs(r-b)<lim
    
    mask = r_g_diff & g_b_diff & r_b_diff
    
    r = r*mask
    g = g*mask
    b = b*mask
    
    return np.stack([b,g,r],axis=2).astype('uint8')