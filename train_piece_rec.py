# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 13:02:43 2019

@author: AMIT
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from test2 import show_imgs,split_img,get_train_data

X_data,y_data = get_train_data()

X_p = X_data.reshape((X_data.shape[0],X_data.shape[1],X_data.shape[2],1))
y_p = y_data[:,0]

from sklearn.preprocessing import OneHotEncoder
hot_encoder = OneHotEncoder(categorical_features=[0])
y_p = hot_encoder.fit_transform(y_p.reshape((y_p.shape[0],1))).toarray()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_p, y_p, test_size=0.2, random_state=0)

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
classifier.add(Dense(128, activation='sigmoid'))
classifier.add(Dense(7, activation='softmax'))

classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

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
                                   horizontal_flip=True,)

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
with open("classifier_piece.pickle","wb") as fil:
    pickle.dump(classifier,fil)

