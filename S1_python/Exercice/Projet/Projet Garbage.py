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
#    globals()['%s' % str(i).split('\\')[-1]] = glob.glob(str(i)+'\\*.jpg')
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
for i in img_grpTEN.keys():
    globals()['%s' % i] = img_grpTEN[i]

#gather all tensors in a list
all = cardboard + glass + metal + paper + plastic + trash

tf_train_set = tf.data.Dataset.from_tensor_slices(all)



