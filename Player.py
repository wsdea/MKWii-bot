# -*- coding: utf-8 -*-
from grabscreen import grab_screen,cv2_show
from directkeys import PressKey,ReleaseKey,KeyList
from getkeys import key_check
import matplotlib.pyplot as plt
import time
import cv2
import sys,os
import numpy as np
import math
from collections import deque
import random

#from pynput.keyboard import Key, Controller
#keyboard = Controller()
#
#def PressKey(key):
#    keyboard.press(key)
#
#def ReleaseKey(key):
#    keyboard.release(key)

class Player:
    def __init__(self,box=None):
        self.k = KeyList()
        self.box = box or (45,37,912,511)
        self.width,self.height = self.box[2]-self.box[0],self.box[3]-self.box[1]
        self.working_screen = None
        self.displaying_screen = None
        
    def straight(self):
        PressKey(self.k['L'])
        ReleaseKey(self.k['F'])
        ReleaseKey(self.k['H'])
        ReleaseKey(self.k['G'])
    
    def left(self):
        if random.randrange(0,3) == 1:
            PressKey(self.k['L'])
        else:
            ReleaseKey(self.k['L'])
        PressKey(self.k['F'])
        ReleaseKey(self.k['G'])
        ReleaseKey(self.k['H'])
    
    def right(self):
        if random.randrange(0,3) == 1:
            PressKey(self.k['L'])
        else:
            ReleaseKey(self.k['L'])
        PressKey(self.k['H'])
        ReleaseKey(self.k['F'])
        ReleaseKey(self.k['G'])
        
    def reverse(self):
        PressKey(self.k['G'])
        ReleaseKey(self.k['F'])
        ReleaseKey(self.k['L'])
        ReleaseKey(self.k['H'])
    
    def forward_left(self):
        PressKey(self.k['L'])
        PressKey(self.k['F'])
        ReleaseKey(self.k['H'])
        ReleaseKey(self.k['G'])
        
    def forward_right(self):
        PressKey(self.k['L'])
        PressKey(self.k['H'])
        ReleaseKey(self.k['F'])
        ReleaseKey(self.k['G'])
    
    def reverse_left(self):
        PressKey(self.k['G'])
        PressKey(self.k['F'])
        ReleaseKey(self.k['L'])
        ReleaseKey(self.k['H'])
    
    def reverse_right(self):
        PressKey(self.k['G'])
        PressKey(self.k['H'])
        ReleaseKey(self.k['L'])
        ReleaseKey(self.k['F'])
    
    def no_keys(self):
        ReleaseKey(self.k['L'])
        ReleaseKey(self.k['F'])
        ReleaseKey(self.k['G'])
        ReleaseKey(self.k['H'])
    
    def stop(self):
        self.no_keys()
        raise Exception('Stopping')
    
    def process_screen(im):
        print('Need to overwrite this "self.process_screen"')
        return im
        
    def decision(self,im):
        print('Need to overwrite this "self.decision"')
        return "None"
                 
    def execute(self,decision):
        funcs = {
                'forward':self.straight,
                 'left':self.left,
                 'right':self.right,
                 'forward_left':self.forward_left,
                 'forward_right':self.forward_right,
                 'reverse_left':self.reverse_left,
                 'reverse_right':self.reverse_right,
                 'reverse':self.reverse,
                 'no_keys':self.no_keys,
                 'stop':self.stop
                 }
        if "C" in key_check():
             funcs['stop']()
        else:
            funcs.get(decision,lambda : "No decision")()
        
    def run(self,wait=True):
        if 'ipykernel' in sys.modules:
            raise Exception('Executable only on cmd')
        if wait:
            for i in range(3,0,-1):
                print(i)
                time.sleep(1)
        while True:
            try:
                t0 = time.clock()
                screen = grab_screen(self.box)
                self.process_screen(screen)
                move = self.decision()
                self.execute(move)
                cv2_show('mkwii',self.displaying_screen)
                print('Move {} ({:.3f}s)'.format(move,time.clock()-t0),end='\r')
            except:
                self.no_keys()
                raise Exception("Stopped on user's request")
                

    
