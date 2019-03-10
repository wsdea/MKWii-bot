# -*- coding: utf-8 -*-
import os,cv2
from grabscreen import im_show

path = 'D:\MKWii datasets'
L = os.listdir(path)
L = [os.path.join(path,x) for x in L if x.split('.')[-1].lower() in ['jpg','jpeg','bmp','png']]
im = cv2.imread(L[5])
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_show(im)
edges = cv2.Canny(im,threshold1=200,threshold2=300)
im_show(edges)





def edge_model(image):
    key = 0
    return key