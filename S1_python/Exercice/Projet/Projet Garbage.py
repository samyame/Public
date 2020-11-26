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
allt = cardboard + glass + metal + paper + plastic #+ trash

#validation set
valt = cardboard[int(len(cardboard)*0.8):] + glass[int(len(glass)*0.8):] + metal[int(len(metal)*0.8):] + paper[int(len(paper)*0.8):] + plastic[int(len(plastic)*0.8):] #+ trash[int(len(trash)*0.8):]

#train set
traint = cardboard[:int(len(cardboard)*0.8)] + glass[:int(len(glass)*0.8)] + metal[:int(len(metal)*0.8)] + paper[:int(len(paper)*0.8)] + plastic[:int(len(plastic)*0.8)] #+ trash[:int(len(trash)*0.8)]

tf_train_set = tf.data.Dataset.from_tensor_slices(traint)

tf_test_set = tf.data.Dataset.from_tensor_slices(valt)

#get labels for images
label_index = {}
for i,j in enumerate(repos):
    label_index[str(j).split('\\')[-1]] = i

labelt = []
for i in traint:
    for j in repos:
        if str(j).split('\\')[-1] in i:
            labelt.append(label_index[str(j).split('\\')[-1]])

labelv = []
for i in valt:
    for j in repos:
        if str(j).split('\\')[-1] in i:
            labelv.append(label_index[str(j).split('\\')[-1]])

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

def load_valid_images(img):
  img = tf.io.read_file(img)
  img = tf.image.decode_jpeg(img, channels=3)
  img = tf.image.resize(img, [100, 100])
  img = img / 255.0
  
  return img

tf_test_set = tf_test_set.map(load_valid_images)

#label into tensors
tf_labels_tr = tf.data.Dataset.from_tensor_slices(labelt)

tf_labels_val = tf.data.Dataset.from_tensor_slices(labelv)


#create full tensor datasets
full_train_ds = tf.data.Dataset.zip((tf_train_set, tf_labels_tr))
full_train_ds = full_train_ds.shuffle(len(traint)).batch(16)

full_val_ds = tf.data.Dataset.zip((tf_test_set, tf_labels_val))
full_val_ds = full_val_ds.shuffle(len(valt)).batch(16)

#Création du modèle

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding="same", activation="relu", input_shape=[150, 150, 3]),
    tf.keras.layers.MaxPool2D(pool_size=2, padding="same"), #, strides=2, padding='valid'),
    tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu"),
    tf.keras.layers.MaxPool2D(pool_size=2, padding="same"), # strides=2, padding='valid'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=32, activation='relu'),
    tf.keras.layers.Dropout(0.05),
    tf.keras.layers.Dense(units=16, activation ="relu"),
    tf.keras.layers.Dense(units=10, activation ="relu"),
    tf.keras.layers.Dense(units=5, activation='softmax')
    ])

model.summary()

initial_learning_rate = 0.0001

lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate,
    decay_steps=6000,
    decay_rate=0.96,
    staircase=True)

model.compile(optimizer = tf.keras.optimizers.Adam(lr_schedule),
              loss= tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics = [tf.keras.metrics.SparseCategoricalAccuracy()])

history = model.fit(full_train_ds, epochs=15, batch_size = 16, validation_data = full_val_ds)

#chercher le learning rate optimal
"""
def create_model():
  model2 = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding="same", activation="relu", input_shape=[100, 100, 3]),
    tf.keras.layers.MaxPool2D(pool_size=2, padding="same"), #, strides=2, padding='valid'),
    tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu"),
    tf.keras.layers.MaxPool2D(pool_size=2, padding="same"), # strides=2, padding='valid'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=32, activation='relu'),
    tf.keras.layers.Dropout(0.05),
    tf.keras.layers.Dense(units=16, activation ="relu"),
    tf.keras.layers.Dense(units=10, activation ="relu"),
    tf.keras.layers.Dense(units=6, activation='softmax')
    ])

  return model

# On teste différentes valeurs entre 0.1 et 10^-6
learning_rates = [.1, .01, .001, .0001, .00001, .000001]
n_epoch = 10

for i,lr in enumerate(learning_rates):

  model2 = create_model()
  
  model2.compile(optimizer=tf.keras.optimizers.Adam(learning_rate = lr),
                loss = tf.keras.losses.SparseCategoricalCrossentropy(),
                metrics = [tf.keras.metrics.SparseCategoricalAccuracy()])
  
  history1 = model2.fit(full_train_ds, 
                      epochs=n_epoch,
                      validation_data = full_val_ds,
                      verbose=0)
  
  plt.plot(history1.history['sparse_categorical_accuracy'], color="b", label='train')
  plt.plot(history1.history['val_sparse_categorical_accuracy'], color="r", label='test')
  plt.title('lrate='+str(lr))
  plt.show()
"""
#save model
cp_callback = tf.keras.callbacks.ModelCheckpoint('cp.ckpt', save_weights_only=True, verbose = 1)

#prediction preprocessing
def prepro(imgs):
    tf_test = tf.data.Dataset.from_tensor_slices(imgs)
    tf_test = tf_test.map(load_valid_images)
    tf_test = tf_test.shuffle(len(imgs)).batch(16)
    
    return tf_test

