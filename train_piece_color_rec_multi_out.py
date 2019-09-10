# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:11:47 2019

@author: AMIT
"""
import numpy as np

X_train = np.load('piece_train_imgdata_short.npy')
y_train = np.load('piece_train_tagdata_short.npy')

# shuffling data
sh_ind = np.arange(X_train.shape[0])
np.random.shuffle(sh_ind)
X_train = X_train[sh_ind]
y_train = y_train[sh_ind]

X_test = np.load('piece_test_imgdata_short.npy')
y_test = np.load('piece_test_tagdata_short.npy')

sh_ind = np.arange(X_test.shape[0])
np.random.shuffle(sh_ind)
X_test = X_test[sh_ind]
y_test = y_test[sh_ind]


import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.callbacks import EarlyStopping

layer_inp = keras.Input(shape=(50,50,1))

layer_int = Conv2D(32, (3,3), activation='relu')(layer_inp)
layer_int = MaxPooling2D(pool_size=(2,2))(layer_int)
layer_int = Flatten()(layer_int)

layer_int = Dense(128, activation='sigmoid')(layer_int)

layer_color_out = Dense(3, activation='softmax', name='outc')(layer_int)
layer_piece_out = Dense(7, activation='softmax', name='outp')(layer_int)

classifier = keras.Model(inputs=layer_inp, outputs=[layer_color_out, layer_piece_out])

losses = {'outc':'categorical_crossentropy', 'outp':'categorical_crossentropy'}
weights = {'outc':1.0, 'outp':1.0}
metrices = {'outc':'accuracy', 'outp':'accuracy'}

classifier.compile(optimizer='adam', loss=losses, loss_weights=weights, metrics=metrices)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   vertical_flip=True,
                                   horizontal_flip=True,)

test_datagen = ImageDataGenerator(rescale=1./255,
                                  zoom_range=0.2,
                                  vertical_flip=True)

def batch_generator(generator):
    while True:
        X_temp, y_temp = next(generator)
        yield X_temp, {'outc':y_temp[:,:3], 'outp':y_temp[:,3:]}

train_datagen.fit(X_train)
training_set = train_datagen.flow(X_train, y_train, batch_size=50)

test_datagen.fit(X_test)
test_set = test_datagen.flow(X_test, y_test, batch_size=50)

early_stopper = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=3, 
                              mode='min', restore_best_weights=True)

classifier.fit_generator(batch_generator(training_set),
                        steps_per_epoch=500,
                        epochs=5,
                        validation_data=batch_generator(test_set),
                        validation_steps=100,
                        callbacks=[early_stopper])
#epochs = 10
#for e in range(epochs):
#    print('Epoch', e)
#    batches = 0
#    for x_batch, y_batch in train_datagen.flow(X_train, y_train, batch_size=50):
#        classifier.fit(x_batch, {'outc':y_batch[:,:3], 'outp':y_batch[:,3:]})
#        batches += 1
#        if batches >= 50:
#            # we need to break the loop by hand because
#            # the generator loops indefinitely
#            break

y_trains = {'outc':y_train[:,:3], 'outp':y_train[:,3:]}
y_tests = {'outc':y_test[:,:3], 'outp':y_test[:,3:]}

classifier.fit(X_train, y_trains, batch_size=50, epochs=40, validation_data=(X_test,y_tests))

