# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 13:43:20 2022

@author: mm180261d
"""

from skimage import filters
import numpy as np
import cv2
import os
from scipy import ndimage

def iseci_slovo(img: np.array) -> np.array:
    """
    

    Parameters
    ----------
    img : np.array
        Ulazna slika.

    Returns
    -------
    img : TYPE
        Izlazna slika na kojoj je smao slovo.

    """
    img = img[10:-10, 10: -10]
    # za secenje okvira
    i = 0
    while np.sum(img[:, i]) < 300:
        img = img[:, i+5:]
    img = img[:, i+5:]
    i = 1
    while np.sum(img[:, -i]) < 300:
        img = img[:, :-i-5]
    img = img[:, :-i-5]
    i=0
    while np.sum(img[i, :]) < 300:
        img = img[i+5:, :]
    img = img[i+5:, :]
    i = 1
    while np.sum(img[-i, :]) < 300:
        img = img[:-i-5, :]
    img = img[:-i-5, :]
    
    # Otsuova granica
    otsu = filters.threshold_otsu(img)
    img[img<=otsu] = 0
    img[img>otsu] = 1
    
    # za secenje slova
    i = 0
    while np.sum(img[:, i]) >= img.shape[0]-5:
        img = img[:, i+1:]
    i = 1
    while np.sum(img[:, -i]) >= img.shape[0]-5:
        img = img[:, :-i]
    
    i=0
    while np.sum(img[i, :]) >= img.shape[1]-5:
        img = img[i+1:, :]
    i = 1
    while np.sum(img[-i, :]) >= img.shape[1]-5:
        img = img[:-i, :]
    
    return img


if __name__=="__main__":
    path = './baza_slova'
    path_output = './baza_slova_izlaz'
    path_images = os.listdir(path)
    i=0
    for path_img in path_images:
        i = i+1
        img = cv2.imread(path + '/' + path_img)/256
        img = img[:, :, 0]
        img = iseci_slovo(img)
        cv2.imwrite(path_output + '/' + path_img, img*256)