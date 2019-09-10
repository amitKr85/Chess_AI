# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 14:28:38 2019

@author: AMIT
"""


import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from test2 import show_imgs,split_img,get_train_data

X_data,y_data = get_train_data()

X_c = X_data.reshape((X_data.shape[0],X_data.shape[1],X_data.shape[2],1))[y_data[:,0]!=0]
y_c = y_data[:,1][y_data[:,0]!=0]
y_c = y_c.reshape((y_c.shape[0],1))

show_imgs(X_c[:64], 8,8,0,title_list=y_c[:64])
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_c, y_c, test_size=0.2, random_state=0)

# making network
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.callbacks import EarlyStopping


classifier = Sequential()
# adding conv. layer
classifier.add(Conv2D(32, (3, 3), input_shape=(50, 50, 1), activation='relu'))
# adding pooling layer
classifier.add(MaxPooling2D(pool_size=(2,2)))
#
##adding 2nd conv. layer to reduce overfitting
#classifier.add(Conv2D(32, (3, 3), activation='relu'))
#classifier.add(MaxPooling2D(pool_size=(2,2)))

# adding flatten layer
classifier.add(Flatten())

# adding fully connected arch.
classifier.add(Dense(64, activation='sigmoid'))
classifier.add(Dense(1, activation='sigmoid'))

classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# adding callbacks
#checkpointer = ModelCheckpoint(filepath='weights.hdf5', verbose=1, save_best_only=True)
early_stopper = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=3, 
                              mode='min', restore_best_weights=True)

#classifier.fit(X_train, y_train, batch_size=50, epochs=25, validation_data=(X_test, y_test))

# augementing images
# to reduce overfitting
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   vertical_flip=True,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255,
                                  zoom_range=0.2,
                                  vertical_flip=True)

train_datagen.fit(X_train)
training_set = train_datagen.flow(X_train, y_train, batch_size=50)

test_datagen.fit(X_test)
test_set = train_datagen.flow(X_test, y_test, batch_size=50)

classifier.fit_generator(training_set,
                        steps_per_epoch=500,
                        epochs=25,
                        validation_data=test_set,
                        validation_steps=100,callbacks=[early_stopper])

import pickle
with open("classifier_piece_color.pickle","wb") as fil:
    pickle.dump(classifier,fil)
    
with open("classifier_piece_color.pickle","rb") as fil:
    classifier = pickle.load(fil)