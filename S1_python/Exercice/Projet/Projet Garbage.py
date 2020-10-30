# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:49:46 2020

@author: Sam
"""

import tensorflow as tf
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import pathlib
import glob
from keras.preprocessing.image import ImageDataGenerator, array_to_img, load_img, img_to_array

#path du repertoire maitre
repo = pathlib.Path(r"C:\Users\tashi\Documents\GitHub\jedha\S1_python\Exercice\Projet\dataset")

#paths des repertoires
repos = list(repo.glob("*/"))

#gather all img paths by type in a dictionary
img_grp = {}
for i in repos:
    globals()['%s' % str(i).split('\\')[-1]] = glob.glob(str(i)+'\\*.jpg')
    img_grp[str(i).split('\\')[-1]] = globals()['%s' % str(i).split('\\')[-1]]

#convert the img paths into bytes
img_grpBY = {}
for i in img_grp.keys():
    img_grpBY[i] = [tf.io.read_file(x) for x in img_grp[i]]

#convert the bytes into tensors    
img_grpTEN = {}
for i in img_grpBY.keys():
    img_grpTEN[i] = [tf.image.decode_jpeg(img) for img in img_grpBY[i]]

#shape of one tensor
shap = list(img_grpTEN['metal'][0].shape)

#sort tensors by type in separate files
#for i in img_grpTEN.keys():
#    globals()['%s' % i] = img_grpTEN[i]


#gather all tensors in a list
allt = cardboard + glass + metal + paper + plastic + trash


tf_train_set = tf.data.Dataset.from_tensor_slices(allt)

#get labels for images
label_index = {}
for i,j in enumerate(repos):
    label_index[str(j).split('\\')[-1]] = i

label = []
for i in allt:
    for j in repos:
        if str(j).split('\\')[-1] in i:
            label.append(label_index[str(j).split('\\')[-1]])

#image preprocessing
def load_and_preprocess_images(img):
  img = tf.io.read_file(img) #convert to bytes
  img = tf.image.decode_jpeg(img, channels=3) #convert to tensor
  img = tf.image.resize(img, [100, 100]) #resize shape
  img = tf.image.random_flip_left_right(img) #
  img = tf.image.random_contrast(img, 0.50, 0.90)
  img = img / 255.0
  
  return img

tf_train_set = tf_train_set.map(load_and_preprocess_images)

tf_labels = tf.data.Dataset.from_tensor_slices(label)

full_ds = tf.data.Dataset.zip((tf_train_set, tf_labels))
full_ds = full_ds.shuffle(len(allt)).batch(16)

#Création du modèle

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu", input_shape=[100, 100, 3]),
    tf.keras.layers.MaxPool2D(pool_size=2, padding="same"), #, strides=2, padding='valid'),
    tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"),
    tf.keras.layers.MaxPool2D(pool_size=2, padding="same"), # strides=2, padding='valid'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=16, activation='relu'),
    tf.keras.layers.Dropout(0.05),
    tf.keras.layers.Dense(units=8, activation ="relu"),
    tf.keras.layers.Dense(units=10, activation ="relu"),
    tf.keras.layers.Dense(units=6, activation='softmax')
    ])

model.summary()

initial_learning_rate = 0.001

lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate,
    decay_steps=6000,
    decay_rate=0.96,
    staircase=True)

model.compile(optimizer = tf.keras.optimizers.Adam(lr_schedule),
              loss= tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics = [tf.keras.metrics.SparseCategoricalAccuracy()])

history = model.fit(full_ds, epochs=100, batch_size = 16)
