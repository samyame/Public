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

#path du repertoire maitre
repo = pathlib.Path(r"C:\Users\tashi\Downloads\Projet\Garbage classification\Garbage classification")

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
  img = tf.io.read_file(img)
  img = tf.image.decode_jpeg(img, channels=3)
  img = tf.image.resize(img, [192, 192])
  img = tf.image.random_flip_left_right(img)
  img = tf.image.random_contrast(img, 0.50, 0.90)
  img = img / 255.0
  
  return img

tf_train_set = tf_train_set.map(load_and_preprocess_images)

tf_labels = tf.data.Dataset.from_tensor_slices(label)

full_ds = tf.data.Dataset.zip((tf_train_set, tf_labels))
full_ds = full_ds.shuffle(len(allt)).batch(16)

