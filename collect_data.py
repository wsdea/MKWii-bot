# -*- coding: utf-8 -*-
import numpy as np
from grabscreen import grab_screen,im_show
import cv2
import time
from getkeys import key_check
import os

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

path = 'D:\MKWii datasets'


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0,0,0,0,0,0,0,0,0]

    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output


def collect_images(path):
    file_name = os.path.join(path,'training_data-{}.jpeg')
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    n_images = 0
    paused = False
    print('STARTING!!!')
    while True:
        if not paused:
            screen = grab_screen()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            cv2.imwrite(file_name.format(int(1000*time.time())),screen)
            n_images += 1
            if n_images % 100 == 0:
                print(n_images)
                
        keys = key_check()
        if 'P' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
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
#
#
#main(file_name, starting_value)

collect_images(path)