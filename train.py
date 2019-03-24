# -*- coding: utf-8 -*-
import os
#import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D,MaxPool2D,Flatten,Dropout,Dense,BatchNormalization
from tensorflow.python.keras.callbacks import TensorBoard,ModelCheckpoint,EarlyStopping,Callback,ReduceLROnPlateau

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random 
random.seed(42)

from utils import load_pickle,remove_content
        
def train_neural_network(training_folder,test_folder="",n_epoch=1,batch_size=32,name=None,path=None):
    remove_content(path)
    
    dataset_list = [os.path.join(training_folder,x) for x in os.listdir(training_folder)]
#    data variables
    h,w = load_pickle(dataset_list[0])[0].shape[1:]
    print(h,w)
    n_classes = 10
    
    model = Sequential()
    model.add(Conv2D(filters=32,kernel_size=(5,5),strides=(3,3),input_shape=(h,w,1),activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPool2D((2,2)))
#    model.add(Dropout(0.3))
    
    model.add(Conv2D(filters=32,kernel_size=(3,3),strides=(1,1),activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPool2D((2,2)))
#    model.add(Dropout(0.3))
#    
#    model.add(Conv2D(filters=64,kernel_size=(1,5),strides=(1,1),activation='relu'))
#    model.add(BatchNormalization())
#    model.add(MaxPool2D((1,2)))
#    model.add(Dropout(0.2))
        
    model.add(Flatten())
    
    model.add(Dense(16,activation='relu'))
#    model.add(Dropout(0.3))
    model.add(Dense(n_classes,activation='softmax'))
    
    model.summary() #prints summary
    
    desc = model.get_config()
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
        
#    # Callbacks
#    checkpoint = ModelCheckpoint(path+'/'+name+'_{epoch:03d}.h5')#, monitor='val_loss')
#    early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=50, verbose=1, mode='min')
#    tensorboard = TensorBoard(log_dir=path+"/logs/{}".format(name))
#    print('Open Tensorboard with cmd : tensorboard --logdir=logs/')
#    
#    X_train = X_train.reshape(X_train.shape[0],1,X_train.shape[1],X_train.shape[2]) #reshaping to an image 1 x n_candlesticks x n_channels
#    X_val = X_val.reshape(X_val.shape[0],1,X_val.shape[1],X_val.shape[2]) #reshaping to an image 1 x n_candlesticks x n_channels
    for epoch in range(1,n_epoch+1):
        print('\nEpoch {}'.format(epoch))
        for dataset_name in dataset_list[:-1]:
            pkl = load_pickle(dataset_name)
            X_train = pkl[0].reshape((-1,h,w,1))
            y_train = pkl[1]
    #        print(X_train.shape,y_train.shape)
            model.fit(
                X_train,y_train,
                epochs=1,
                batch_size = batch_size,
                shuffle=True,
                verbose=2,
    #            callbacks=[early_stop]
    #            callbacks=[early_stop,tensorboard]
                )
        model.save("{}/{}_{}.h5".format(path, name,epoch))
    
    return model

######################################################
def main():    
    
    ##################################################################################
    #Parameters
    ##################################################################################
    
    name = 'model'
    path = r"models\current_model"
    training_folder = r"D:\MKWii datasets"
    n_epoch = 2
    batch_size = 64
    model = train_neural_network(training_folder,n_epoch = n_epoch,batch_size=batch_size,path=path,name=name)
    model.save("{}/{}.h5".format(path, name))
    
if __name__ == '__main__':
    main()
    
