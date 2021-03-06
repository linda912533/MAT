#!/usr/bin/env python

from __future__ import print_function

import scipy.io as sio
import numpy as np
import struct
from array import array as pyarray
from PIL import Image

from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers import Input, Dense, Dropout, Activation, Flatten, UpSampling2D, Deconvolution2D, ZeroPadding2D
from keras.layers import Convolution2D, MaxPooling2D
from keras import backend as K
from keras.utils import np_utils


# for mnist
from keras.datasets import mnist
import tensorflow as tf



batch_size = 128
nb_classes = 10
nb_epoch = 12
img_channels = 1

# input image dimensions
img_rows, img_cols = 28, 28
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
nb_pool = 2
# convolution kernel size
nb_conv = 3

def read_dataset():

    # parameters for neural network
    batch_size = 128
    nb_classes = 10
    nb_epoch = 6

    # input image dimensions
    img_rows, img_cols = 28, 28
    # number of convolutional filters to use
    nb_filters = 32
    # size of pooling area for max pooling
    nb_pool = 2
    # convolution kernel size
    nb_conv = 3

    # the data, shuffled and split between train and test sets
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    if K.backend() == 'tensorflow':
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, img_channels)
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, img_channels)
    else:
        X_train = X_train.reshape(X_train.shape[0], img_channels, img_rows, img_cols)
        X_test = X_test.reshape(X_test.shape[0], img_channels, img_rows, img_cols)
    
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255
    #print('X_train shape:', X_train.shape)
    #print(X_train.shape[0], 'train samples')
    #print(X_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)
   
    #print('X_train_S:', X_train.shape)
    #print('Y_train_S:', Y_train.shape, 'Y_test_S:', Y_test.shape)

    return (X_train,Y_train,X_test,Y_test, batch_size, nb_epoch)

    
def build_model():
    """
    define neural network model
    """
    
    if K.backend() == 'tensorflow': 
        K.set_learning_phase(0)
    
    if K.backend() == 'tensorflow': 
        inputShape = (img_rows,img_cols,img_channels)
    else: 
        inputShape = (img_channels,img_rows,img_cols)

    
    model_p = Sequential()

    model_p.add(Convolution2D(nb_filters, nb_conv, nb_conv,
                            border_mode='valid',
                            input_shape=inputShape))
    model_p.add(Activation('relu'))
    model_p.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model_p.add(Activation('relu'))
    model_p.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model_p.add(Dropout(0.25))

    model_p.add(Flatten())
    model_p.add(Dense(128))
    model_p.add(Activation('relu'))
    model_p.add(Dropout(0.5))
    model_p.add(Dense(nb_classes))
    model_p.add(Activation('softmax'))

    model_p.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    return model_p
    

    
"""
   The following function gets the activations for a particular layer
   for an image in the test set. 
   FIXME: ideally I would like to be able to 
          get activations for a particular layer from the inputs of another layer. 
"""

def getImage(model,n_in_tests):

    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    if K.backend() == 'tensorflow': 
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    else: 
        X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    X_test = X_test.astype('float32')
    X_test /= 255
    
    Y_test = np_utils.to_categorical(y_test, nb_classes)
    #print('X_test shape:', X_test.shape, ' 0:', X_test.shape[0], ' 1:', X_test.shape[1])
    image = X_test[n_in_tests:n_in_tests+1]
    #print('image shape:', image.shape, ' 0:', image.shape[0], ' 1:', image.shape[1])
    #print('image[0] shape:', image[0].shape, ' 0:', image[0].shape[0], ' 1:', image[0].shape[1])
    if K.backend() == 'tensorflow':
        return image[0]
    else: 
        return np.squeeze(image)
    
def getImages(model,n_in_tests1,n_in_tests2):

    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    if K.backend() == 'tensorflow': 
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    else: 
        X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    X_test = X_test.astype('float32')
    X_test /= 255
    
    Y_test = np_utils.to_categorical(y_test, nb_classes)
    image2 = X_test[n_in_tests1:n_in_tests2]
    return np.squeeze(image2)
    
def getLabel(model,n_in_tests):

    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    if K.backend() == 'tensorflow': 
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    else: 
        X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    X_test = X_test.astype('float32')
    X_test /= 255
    
    Y_test = np_utils.to_categorical(y_test, nb_classes)
    image = Y_test[n_in_tests:n_in_tests+1]
    if K.backend() == 'tensorflow':
        return image[0]
    else: 
        return np.squeeze(image)
    
def readImage(path):
    
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import numpy as np
    import PIL
    from PIL import Image
    img=rgb2gray(mpimg.imread(path))
        
    img = img.resize((img_cols, img_rows))
    return np.squeeze(img)
    
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def getActivationValue(model,layer,image):

    if len(image.shape) == 2: 
        image = np.expand_dims(np.expand_dims(image, axis=0), axis=0)
    elif len(image.shape) == 3: 
        image = np.expand_dims(image, axis=0)
    activations = get_activations(model, layer, image)
    return np.squeeze(activations)

    
def get_activations(model, layer, X_batch):
    get_activations = K.function([model.layers[0].input, K.learning_phase()], model.layers[layer].output)
    activations = get_activations([X_batch,0])
    return activations

def predictImage(model, image):
	
    ## image(28, 28)
    #print('pre img shape', image.shape)
    img = np.expand_dims(np.expand_dims(image, axis=2), axis=0)

    
    img_pre = model.predict(img)
    newClass = np.argmax(np.ravel(img_pre))
    confident = np.amax(np.ravel(img_pre))
    
    return (newClass, confident)
    
def predictWithImage(model,newInput):

    if len(newInput.shape) == 2 and K.backend() == 'tensorflow': 
        newInput2 = np.expand_dims(np.expand_dims(newInput, axis=2), axis=0)
    elif len(newInput.shape) == 2 and K.backend() == 'theano': 
        newInput2 = np.expand_dims(np.expand_dims(newInput, axis=0), axis=0)
    else: 
        newInput2 = np.expand_dims(newInput, axis=0)
    predictValue = model.predict(newInput2)
    #print('predict:', predictValue)
    newClass = np.argmax(np.ravel(predictValue))
    confident = np.amax(np.ravel(predictValue))
    return (newClass,confident)    
    
def getWeightVector(model, layer2Consider):
    weightVector = []
    biasVector = []

    for layer in model.layers:
         index=model.layers.index(layer)
         h=layer.get_weights()
         
         if len(h) > 0 and index in [0,2]  and index <= layer2Consider: 
         # for convolutional layer
             ws = h[0]
             bs = h[1]
             
             # number of filters in the previous layer
             m = len(ws)
             # number of features in the previous layer
             # every feature is represented as a matrix 
             n = len(ws[0])
             
             for i in range(1,m+1):
                 biasVector.append((index,i,h[1][i-1]))
             
             for i in range(1,m+1):
                 v = ws[i-1]
                 for j in range(1,n+1): 
                     # (feature, filter, matrix)
                     weightVector.append(((index,j),(index,i),v[j-1]))
                     
         elif len(h) > 0 and index in [7,10]  and index <= layer2Consider: 
         # for fully-connected layer
             ws = h[0]
             bs = h[1]
             
             # number of nodes in the previous layer
             m = len(ws)
             # number of nodes in the current layer
             n = len(ws[0])
             
             for j in range(1,n+1):
                 biasVector.append((index,j,h[1][j-1]))
             
             for i in range(1,m+1):
                 v = ws[i-1]
                 for j in range(1,n+1): 
                     weightVector.append(((index-1,i),(index,j),v[j-1]))
         #else: print "\n"
         
    return (weightVector,biasVector)        

def getConfig(model):

    config = model.get_config()
    # print('config in getConfig: ', config)
    if 'layers' in config: config = config['layers']
    config = [ getLayerName(dict) for dict in config ]
    config = zip(range(len(config)),config)
    return config 
    
def getLayerName(dict):

    className = dict.get('class_name')
    if className == 'Activation': 
        return dict.get('config').get('activation')
    else: 
        return className
