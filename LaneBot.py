# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 23:24:51 2019

@author: willi
"""
from Player import Player
from utils import grab_screen,cv2_show

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
        self.last_points = deque(maxlen=5)

    def ROI(self,im):
        horizon_mask = np.zeros_like(im)
        cv2.fillPoly(horizon_mask,[np.array(self.horizon_vertices)],255)
        masked = cv2.bitwise_and(im,horizon_mask)
        
        if not self.player_vertices is None:
            player_mask = np.zeros_like(im)+255
            cv2.fillPoly(player_mask,[np.array(self.player_vertices)],0)
            masked = cv2.bitwise_and(masked,player_mask)
        
        return masked
    
    def create_line(self,slope,bias):
        #basically we want to draw the line from the top to the bottom
        fm = lambda y : int(round((y-bias)/slope)) #f-1
        f = lambda x : int(round(slope*x+bias))
        
        w = self.width-1
        h = self.height-1
        f0 = int(round(bias))
        fw = f(w)
        fm0 = fm(0)
        fmh = fm(h)
        
        up = (fm0,0)
        down = (fmh,h)
        right = (w,fw)
        left = (0,f0)
        
        if f0 < 0: #up, y = 0
            x1,y1 = up
            if fw < h: #right x = w
                x2,y2 = right
            else: #down y = h
                x2,y2 = down
        elif f0 < h: #left x = 0
            x1,y1 = left
            if fw < 0:  #up
                x2,y2 = up
            elif fw < h:
                x2,y2 = right
            else: #fw>h -> down
                x2,y2 = down
        else: #f0 > h
            x1,y1 = down
            if fw < 0:
                x2,y2 = up
            elif fw < h:
                x2,y2 = right
            else:
                raise Exception('Impossible case')
        
        return [[x1,y1,x2,y2]]

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
        
#        print(S)
#        print(B)
#        print(lines)
        
        if len(lines)==0:
            return lines,(self.width//2,0)
        
        #grouping similar lines
#        grouped_lines = [lines[0]]
        S_G = np.array([S[0]])
        B_G = np.array([B[0]])
        grouped_lines = np.array([self.create_line(S[0],B[0])])
#        print('s',S[0],'b',B[0])
#        print("g",grouped_lines)
#        print(lines[:1])
#        return grouped_lines,np.array([self.width//2,0])
        count = np.array([1])
        for i in range(1,len(lines)):
            grouped = False
            for j in range(len(S_G)):
                if abs(S[i]-S_G[j])<0.15:# and abs(B[i]-B_G[j])<15: #lines are similar
                    S_G[j] = (S_G[j] * count[j] + S[i])/(count[j]+1)
                    B_G[j] = (B_G[j] * count[j] + B[i])/(count[j]+1)
                    grouped_lines[j] = np.array([self.create_line(S_G[j],B_G[j])])
                    count[j] += 1
                    grouped = True
                    break #we go to the non grouped line
                
            #we have gone through all the grouped lines
            if not grouped: #this line is unique so we add another group
                grouped_lines = np.concatenate([grouped_lines,[self.create_line(S[i],B[i])]])
                S_G = np.append(S_G,S[i])
                B_G = np.append(B_G,B[i])
                count = np.append(count,1)
        
#        print('\n')
#        print('g',grouped_lines)
#        print(S_G)
#        print(B_G)
                    
                
        if len(grouped_lines) == 1: #not able to cross, so we need to decide where to go now
            if abs(S_G[0]) > 0.3: #straight
                return grouped_lines,(self.width//2,0)
            elif S_G[0] > 0: #we need to go left
                return grouped_lines,np.array([0,0]) 
            else: #we need to go right
                return grouped_lines,np.array([0,self.width-1]) 
                    
        full_A = np.ones((S_G.size,2))
        full_A[:,0] = -S_G
        
        ATA = full_A.T.dot(full_A)
        ATb = full_A.T.dot(B_G)
        
    #    mean_point = np.linalg.inv(ATA).dot(ATb).astype('int')
        mean_point,_,_,_ = np.linalg.lstsq(ATA,ATb)
        if not (mean_point[0] >= 0 and mean_point[0] < self.width and mean_point[1] >= 0 and mean_point[1] < self.height):
            return grouped_lines,np.array([self.width//2,0])
        else:
            return grouped_lines,np.array(mean_point)
    
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
        if x >= w+10:
            return 'right'
        elif x <= w-10:
            return 'left'
        else:
            return 'forward'
        
bot = LaneBot()
bot.run()


