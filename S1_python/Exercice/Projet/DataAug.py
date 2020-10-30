# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:21:38 2020

@author: Sam
"""
import pathlib
import glob
from keras.preprocessing.image import ImageDataGenerator, array_to_img, load_img, img_to_array


#path du repertoire maitre
repo = pathlib.Path(r"C:\Users\tashi\Downloads\Projet\Garbage classification\Garbage classification")

#paths des repertoires
repos = list(repo.glob("*/"))

img_grp = {}
for i in repos:
    globals()['%s' % str(i).split('\\')[-1]] = glob.glob(str(i)+'\\*.jpg')
    img_grp[str(i).split('\\')[-1]] = globals()['%s' % str(i).split('\\')[-1]]

for rep in img_grp.keys():
    for path in img_grp[rep]: 
        datagen = ImageDataGenerator(
                rotation_range = 40,
                width_shift_range = 0.2,
                height_shift_range = 0.2,
                shear_range = 0.2,
                zoom_range = 0.2,
                horizontal_flip = True,
                fill_mode = 'nearest')
        
        img = load_img(path)
        x = img_to_array(img)
        x = x.reshape((1,)+x.shape)
        
        i = 0
        for batch in datagen.flow(x, batch_size = 1, save_to_dir = "dataset/" +str(rep), save_prefix = 'aug', save_format = '.jpg'):
            i+=1
            if i > 4:
                break