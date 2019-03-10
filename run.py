# -*- coding: utf-8 -*-
from grabscreen import grab_screen
import matplotlib.pyplot as plt
import time
import cv2
import sys
import math

def is_Spyder():
    return 'ipykernel' in sys.modules

if is_Spyder():
    raise Exception('Executable only on cmd')

box = (45,37,912,511)
vertices = []
plt.figure()

def ROI(im):
    #crops the image to what is under the text
    return im[133:,:]

def addLines(im,lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(im,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],3)
    except:
        pass

def process_image(im):
    im = ROI(im)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.Canny(im,threshold1=200,threshold2=300)
    im = cv2.GaussianBlur(im,(5,5),0)
    lines = cv2.HoughLinesP(im, 1, math.pi/180, 100, 5000, 15)
    addLines(im,lines)
    return im

while True:
    t0 = time.clock()
    screen = grab_screen(box)
    processed = process_image(screen)
    cv2.imshow('mkwii',processed)
    cv2.waitKey(25)
    print('Took {:.3f} sec'.format(time.clock()-t0))
    

    
