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
import tensorflow as tf
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class CNNbot(Player):
    def __init__(self,path,model_name = 'model.h5'):
        super().__init__()
        self.R = 4
        self.height,self.width = round((self.box[3]-self.box[1])/self.R),round((self.box[2]-self.box[0])/self.R)
        tf.keras.backend.clear_session()
        self.model_folder = path
        self.model_name = model_name
        self.model = tf.keras.models.load_model(os.path.join(self.model_folder,self.model_name))
    
    def process_screen(self,im):
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.resize(im,(self.width,self.height), interpolation=cv2.INTER_LINEAR)
        self.displaying_screen = im.copy()
        im = im.reshape(1,im.shape[0],im.shape[1],1)
        self.working_screen = im
    
    def decision(self):
        pred = self.model.predict(self.working_screen)[0]
        action = np.argmax(pred)
        return list(self.actions.keys())[action]


bot = CNNbot(path="models\current_model",model_name='model_1.h5')
bot.run(False)


