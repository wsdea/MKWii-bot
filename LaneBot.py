# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 23:24:51 2019

@author: willi
"""
from Player import Player
from grabscreen import grab_screen,cv2_show

import time
import cv2
import os
import numpy as np
import math
from collections import deque

class LaneBot(Player):
    def __init__(self):
        super().__init__()
        self.horizon_vertices = [[0,121],[167,121],[430,60],[670,121],[866,121],[866,473],[0,473]]
        self.player_vertices = [[489,407],[489,194],[378,194],[378,407]]
#        self.player_vertices = None
        self.last_points = deque(maxlen=10)

    def ROI(self,im):
        horizon_mask = np.zeros_like(im)
        cv2.fillPoly(horizon_mask,[np.array(self.horizon_vertices)],255)
        masked = cv2.bitwise_and(im,horizon_mask)
        
        if not self.player_vertices is None:
            player_mask = np.zeros_like(im)+255
            cv2.fillPoly(player_mask,[np.array(self.player_vertices)],0)
            masked = cv2.bitwise_and(masked,player_mask)
        
        return masked

    def addLines(self,im,lines):
        try:
            for line in lines:
                coords = line[0]
                cv2.line(im,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],3)
        except:
            pass
            
    def target_point(self,lines):
        if lines is None:
            return lines,(self.width//2,0)
        
        L = lines.reshape((-1,4))
        X1 = L[:,0]
        Y1 = L[:,1]
        X2 = L[:,2]
        Y2 = L[:,3]
        
        S = (Y2-Y1)/(X2-X1) #slope
        B = Y1 - S*X1 #bias
        A = -np.arctan(S)*180/math.pi % 180 #angle
        
        LEFT = (X1 < self.width // 2) & (X2 < self.width // 2) & (S < 0)
        RIGHT = (X1 > self.width // 2) & (X2 > self.width // 2) & (S > 0)
        RELEVANT = ~(A < 3) | (A > 180-3)
        FINITE_SLOPE = np.isfinite(S)
        
        filt = (LEFT | RIGHT) & RELEVANT & FINITE_SLOPE
    #    filt = RELEVANT
        
        lines = lines[filt]
        S = S[filt]
        B = B[filt]
        
        full_A = np.ones((S.size,2))
        full_A[:,0] = -S
        
        ATA = full_A.T.dot(full_A)
        ATb = full_A.T.dot(B)
        
    #    mean_point = np.linalg.inv(ATA).dot(ATb).astype('int')
        mean_point,_,_,_ = np.linalg.lstsq(ATA,ATb)
        if not (mean_point[0] >= 0 and mean_point[0] < self.width and mean_point[1] >= 0 and mean_point[1] < self.height):
            return lines,np.array([self.width//2,0])
        else:
            return lines,np.array(mean_point)
    
    def process_screen(self,im):
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        self.displaying_screen = im
        edges = cv2.Canny(im,threshold1=200,threshold2=300)
        edges = self.ROI(edges)
        edges = cv2.GaussianBlur(edges,(3,3),0)
        self.working_screen = edges.copy()
    
    def decision(self):
        lines = cv2.HoughLinesP(self.working_screen, 1, math.pi/180, 100, minLineLength=100, maxLineGap=10)
        lines, target = self.target_point(lines) #lines are filtered now
        self.last_points.append(target)
        mean_point = np.mean(self.last_points,axis=0)
        mean_point = tuple(mean_point.astype('int'))
        
        self.addLines(self.displaying_screen,lines)
        cv2.circle(self.displaying_screen,mean_point,10,[255,0,255], thickness=3)
        
        return self.decision_with_circle(mean_point)
    
    def decision_with_circle(self,mean_point):
        [x,y] = mean_point
#        print(mean_point)
        w = self.width//2
#        h = self.height//2h
        if x >= w + 40:
            return 'forward_right'
        elif x <= w - 40:
            return 'forward_left'
        else:
            return 'forward'
        
bot = LaneBot()
bot.run()


