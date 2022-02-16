
"""
Created on Mon Nov 23 11:04:23 2020

@author: Sam
"""

from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import load_img, img_to_array
import random
from tkinter import *


#Image Fail
imag = 'Henni.jpg'
img = load_img(imag)
x = img_to_array(img)/255

#Data Preparation
filename = r'C:\Users\tashi\Documents\Vocab - Feuille 1.csv'
filename2 = r'C:\Users\tashi\Documents\Vocab - Grammar.txt'
filename3 = 'difficult_record.csv'
df1 = pd.read_csv(filename, header = 0)
df1 = df1.iloc[:,:3]
col = ['jp','kotoba','en']
df1.columns = col
df2 = pd.read_csv(filename2, header = None, sep = ';', error_bad_lines=False)
df2 = df2.drop(columns = 3)
df2 = df2.drop(df2[df2[2].isna()])
for i in df2.columns:
    df2[i] = df2[i].str.replace('\t','')
df2.columns = ['jp','en','kotoba']
difficult = []
#df = pd.concat([df1,df2], axis = 0, ignore_index = True)




df3 = pd.read_csv(filename3, index_col = 0)




#Test
def test():
#Choice of modes    
    GramVoc = input('Vocab or Grammar? V/G')
    if GramVoc.upper() == 'V':
        df = df1
    elif GramVoc.upper() == 'G':
        df = df2
    size = int(input('How many questions?'))

    df['en'] = df['en'].str.strip()
    df['kotoba'] = df['kotoba'].str.strip()

#    mode = tkinter.entry
    mode = input('Do you wanna practice English or Japanese? E/J\n') #Selection of the language to be tested
    mode2 = input('Review difficult words? Y/N') #Selection for the difficulty
    if mode.upper() == 'J':
        inpu = 'jp'
        outpu = 'en'
    elif mode.upper() == 'E': 
        inpu = 'en'
        outpu = 'jp'
    if mode2.upper() == 'Y':
        daf = df3
    else:
        daf = df
    score = 0
    false = {}
    for ind,i in enumerate(np.random.randint(len(daf),size=size)):
            num_prop = np.random.randint(len(daf),size=4) #4 propositions randomly selected
            prop = list(np.append(num_prop,i)) #Append random propositions with the true answer 
            random.shuffle(prop) #Shuffle answers
            print('\nQuestion {}: {}\n'.format(ind+1,daf[inpu].iloc[i])) #Print question from the selected language column
            for k,j in enumerate(daf[outpu].iloc[prop].unique()): #Print the different propositions from the target language column
                print(k+1,j)
            resp = input('Enter number :\n\n')
            try:
                if daf[outpu].iloc[prop[int(resp)-1]] == daf[outpu].iloc[i]: #Try if answered index matches the right answer 
                    print('\ncorrect!\n\nPhonetic:{}\n'.format(daf['kotoba'].iloc[i])) #Print the right answer from the phonetic column
                    score += 1
                else:
                    print('\nincorrect: {}\n\nPhonetic: {}\n'.format(daf[outpu].iloc[i].capitalize(),daf['kotoba'].iloc[i])) #Print the right answer from the target column
                    false[daf[inpu].iloc[i]] = [daf['kotoba'].iloc[i],daf[outpu].iloc[i]] #Print the right answer from the phonetic column
            except :
                print('\n{}\n\nPhonetic: {}\n'.format(daf[outpu].iloc[i].capitalize(),daf['kotoba'].iloc[i]))
                false[daf[inpu].iloc[i]] = [daf['kotoba'].iloc[i],daf[outpu].iloc[i]]
            
    sco(score, size, false)
    sav(false = false)
    return difficult.append(list(false.keys()))

#Feature to search the meaning of a word
def srh():
    x = input('Enter Word:')
    if len(df.jp[df.jp.str.contains(str(x))]) != 0 or len(df.jp[df.jp.str.contains(str(x).capitalize())]) != 0:
        print('{}'.format(df.en[df.jp.str.contains(str(x))]))
    elif len(df.en[df.en.str.contains(str(x))]) != 0 or len(df.en[df.en.str.contains(str(x).capitalize())]) != 0:
        print('{}'.format(df['jp'][df.en.str.contains(str(x)+'|'+str(x).capitalize())]))


#Saving of difficult words
def sav(false):
    false = false
    difen = []
    difjp = []
    kotob = []
    for i in list(false.keys()):
        print(i)
        if i in df['en'].to_list():
            difen.append(i)
            difjp.append(df['jp'].iloc[df['en'][df['en']==i].index[0]])
            kotob.append(df['kotoba'].iloc[df['en'][df['en']==i].index[0]])
        else:
            difjp.append(i)
            difen.append(df['en'].iloc[df['jp'][df['jp']==i].index[0]])
            kotob.append(df['kotoba'].iloc[df['jp'][df['jp']==i].index[0]])
    difen = difen + list(df3['en'])
    difjp = difjp + list(df3['jp'])
    kotob = kotob + list(df3['kotoba'])

    
    df4 = pd.DataFrame({'jp':difjp, 'en':difen, 'kotoba':kotob,'Count en':[difen.count(x) if x != "None" else 0 for x in difen], 'Count jp':[difjp.count(x) if x != "None" else 0 for x in difjp]})
    df4.to_csv('difficult_record.csv')


#Calculate the score
def sco(score, size, false):
    if score == size:
        print('Your score is a perfect {}/{}! Felicitations puceau!'.format(score,size))
        
    elif score > 0:
        print('Your score is {}/{}'.format(score,size))
        print('Your mistakes:\n\n')
        for obj in false.keys():
            print('{}:\n{}\n{}\n\n'.format(obj, false[obj][0],false[obj][1]))
    else:
        print('Your score is {}/{}'.format(score,size))
        plt.imshow(x, interpolation='nearest')
        plt.title("Tu as marqué {} buts sur {} caviars comme Martial! Nul Germain nuuul!".format(score,size))
        plt.axis('off')
        print('Your mistakes:\n\n')
        for obj in false.keys():
            print('{}:\n{}\n{}\n\n'.format(obj, false[obj][0],false[obj][1]))