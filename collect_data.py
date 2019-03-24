# -*- coding: utf-8 -*-
import numpy as np
from utils import grab_screen,box,save_pickle
import cv2
import time
from getkeys import key_check
import os

forward        = np.array([1,0,0,0,0,0,0,0,0,0]) #0
left           = np.array([0,1,0,0,0,0,0,0,0,0]) #1
right          = np.array([0,0,1,0,0,0,0,0,0,0]) #2
forward_left   = np.array([0,0,0,1,0,0,0,0,0,0]) #3
forward_right  = np.array([0,0,0,0,1,0,0,0,0,0]) #4
backward       = np.array([0,0,0,0,0,1,0,0,0,0]) #5
backward_left  = np.array([0,0,0,0,0,0,1,0,0,0]) #6
backward_right = np.array([0,0,0,0,0,0,0,1,0,0]) #7
item           = np.array([0,0,0,0,0,0,0,0,1,0]) #8
nokey          = np.array([0,0,0,0,0,0,0,0,0,1]) #9

path = 'D:\MKWii datasets'

def keys_to_onehot(keys):
    '''
    Convert keys to a ...multi-hot... array
    '''

    if 'L' in keys: #forward
        if 'H' in keys:
            return forward_right
        elif 'F' in keys:
            return forward_left
        else:
            return forward
    elif 'P' in keys: #backward/drift
        if 'H' in keys:
            return backward_right
        elif 'F' in keys:
            return backward_left
        else:
            return backward
    elif 'H' in keys:
        return right
    elif 'F' in keys:
        return left
    else:
        return nokey


def collect_images(path,R=8):
    file_name = os.path.join(path,'training_data-{}.jpeg')
    for i in range(3,0,-1):
        print(i)
        time.sleep(1)

    n_images = 0
    paused = False
    print('STARTING!!!')
    while True:
        if not paused:
            screen = grab_screen(box)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen,(0,0), fx=1/R,fy=1/R, interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(file_name.format(int(1000*time.time())),screen)
            n_images += 1
            if n_images % 100 == 0:
                print(n_images)
                
        keys = key_check()
        if 'C' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
        time.sleep(0.1)
#    
        
def create_datasets(path):
    for i in range(3,0,-1):
        print(i)
        time.sleep(1)
    
    starting_time = int(time.time())
    file_name = os.path.join(path,'{}-{}.pkl'.format(starting_time,'{}'))
    
    R = 4
    h,w = round((box[3]-box[1])/R),round((box[2]-box[0])/R)
    n_datasets = 0
    dataset_size = 1000
    n_images = 0
    training_data = (np.zeros((dataset_size,h,w)),np.zeros((dataset_size,10)))
    print(training_data[0].shape)
    print(training_data[1].shape)
    paused = False
    print('STARTING!!!')
    while True:
        keys = key_check()
        if 'C' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
                
        if not paused:
            screen = grab_screen(box)
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen,(w,h), interpolation=cv2.INTER_LINEAR)
                 
            output = keys_to_onehot(keys)
            training_data[0][n_images] = screen.copy()
            training_data[1][n_images] = output.copy()
            n_images += 1
            
            if n_images % 100 == 0:
                print(n_images)
                
                if n_images == dataset_size:
                    save_pickle(training_data,file_name.format(n_datasets))
                    print('SAVED')
                    training_data = (np.zeros((dataset_size,h,w)),np.zeros((dataset_size,10)))
                    n_datasets += 1
                    n_images = 0
               
        
        time.sleep(0.1)
        
#def main(path, starting_value):
#    file_name = os.path.join(path,'training_data-{}.npy')
#    starting_value = starting_value
#    training_data = []
#    for i in list(range(4))[::-1]:
#        print(i+1)
#        time.sleep(1)
#
#    last_time = time.time()
#    paused = False
#    print('STARTING!!!')
#    while(True):
#        
#        if not paused:
#            screen = grab_screen()
#            last_time = time.time()
#            # resize to something a bit more acceptable for a CNN
##            screen = cv2.resize(screen, (480,270))
#            # run a color convert:
##            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
#            
#            keys = key_check()
#            output = keys_to_output(keys)
#            training_data.append([screen,output])
#
#            #print('loop took {} seconds'.format(time.time()-last_time))
#            last_time = time.time()
###            cv2.imshow('window',cv2.resize(screen,(640,360)))
###            if cv2.waitKey(25) & 0xFF == ord('q'):
###                cv2.destroyAllWindows()
###                break
#
#            if len(training_data) % 100 == 0:
#                print(len(training_data))
#                
#                if len(training_data) == 500:
#                    np.save(file_name,training_data)
#                    print('SAVED')
#                    training_data = []
#                    starting_value += 1
#                    file_name = 'X:/pygta5/phase7-larger-color/training_data-{}.npy'.format(starting_value)
#
#                    
#        keys = key_check()
#        if 'T' in keys:
#            if paused:
#                paused = False
#                print('unpaused!')
#                time.sleep(1)
#            else:
#                print('Pausing!')
#                paused = True
#                time.sleep(1)


#collect_images(path)
create_datasets(path)