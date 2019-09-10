# -*- coding: utf-8 -*-
"""
Created on Thu May 23 02:32:21 2019

@author: AMIT
"""
import numpy as np

datalist_np = None
for data_file in ["datalist_np_20000.npy"]:
    if datalist_np is None:
        datalist_np = np.load(data_file)
    else:
        datalist_np = np.concatenate([datalist_np,np.load(data_file)],axis=0)
        
#datalist_np = np.load("datalist_np_1000.npy")

X = datalist_np[:,:12*64]
y = datalist_np[:,12*64:]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X[:100000],y[:100000], test_size=0.1, random_state=0)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

import keras
from keras.models import Sequential
from keras.layers import Dense

#classifier = Sequential()
#classifier.add(Dense(512,kernel_initializer='uniform',activation='sigmoid',input_shape=(768,)))
#
#classifier.add(Dense(64,kernel_initializer='uniform',activation='softmax'))
#
#classifier.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
#
#classifier.fit(X_train, y_train, batch_size=50, epochs=20, validation_data=(X_test,y_test))



layer_in = keras.Input(shape=(768,))

layer_x = Dense(512,kernel_initializer='uniform',activation='sigmoid')(layer_in)

layer_out_1 = Dense(64, kernel_initializer='uniform', activation='softmax', name='out1')(layer_x)
layer_out_2 = Dense(64, kernel_initializer='uniform', activation='softmax', name='out2')(layer_x)
layer_out_3 = Dense(4, kernel_initializer='uniform', activation='softmax', name='out3')(layer_x)

classifier = keras.Model(inputs=layer_in, outputs=[layer_out_1, layer_out_2, layer_out_3])

losses = {'out1':'categorical_crossentropy', 'out2':'categorical_crossentropy','out3':'categorical_crossentropy'}
weights = {'out1':1.0, 'out2':1.0, 'out3':1.0}
metrices = {'out1':'accuracy', 'out2':'accuracy', 'out3':'accuracy'}

y_trains = {'out1':y_train[:,:64], 'out2':y_train[:,64:128], 'out3':y_train[:,128:]}
y_tests = {'out1':y_test[:,:64], 'out2':y_test[:,64:128], 'out3':y_test[:,128:]}


classifier.compile(optimizer='adam', loss=losses, loss_weights=weights, metrics=metrices)

history2=classifier.fit(X_train, y_trains, batch_size=50, epochs=40, validation_data=(X_test,y_tests))

import matplotlib.pyplot as plt

def plot_hist(hist):
    plt.figure(str(hist))
    plt.plot(hist.history['out1_acc'],label='out1')
    plt.plot(hist.history['out2_acc'],label='out2')
    plt.plot(hist.history['out3_acc'],label='out3')

    plt.plot(hist.history['val_out1_acc'],label='val_out1')
    plt.plot(hist.history['val_out2_acc'],label='val_out2')        
    plt.plot(hist.history['val_out3_acc'],label='val_out3')        
    
    plt.xlabel('epochs')
    plt.ylabel('accuracy')
    plt.legend()
    
    plt.show()
    
plot_hist(history2)

import pickle
with open("classifier_new_temp.pickle","wb") as file:
    pickle.dump(classifier, file)
with open("classifier_scaler_game.pickle","wb") as file:
    pickle.dump(scaler, file)

