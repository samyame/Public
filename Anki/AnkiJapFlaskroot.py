
"""
Created on Mon Nov 23 11:04:23 2020

@author: Sam
"""

from sys import modules
from types import ModuleType
import pandas as pd
import numpy as np
import random


#Data Preparation
filename = r'C:\Users\tashi\Documents\Vocab - Feuille 1.csv'
filename2 = r'C:\Users\tashi\Documents\Vocab - Grammar.txt'
filename3 = 'difficult_record.csv'
df1 = pd.read_csv(filename, header = 0)
df1 = df1.iloc[:,:3]
col = ['jp','kotoba','en']
df1.columns = col
for i in df1.columns:
    df1[i] = df1[i].str.capitalize()
    globals()['df1%s' % i] = df1[i].to_list()
df2 = pd.read_csv(filename2, header = None, sep = ';', error_bad_lines=False)
df2 = df2.drop(columns = 3)
df2 = df2.drop(df2[df2[2].isna()])
df2.columns = ['jp','en','kotoba']
for i in df2.columns:
    df2[i] = df2[i].str.replace('\t','')
    df2[i] = df2[i].str.capitalize()
    globals()['df2%s' % i] = df2[i].to_list()
difficult = []
#df = pd.concat([df1,df2], axis = 0, ignore_index = True)
#df3 = pd.read_csv(filename3, index_col = 0)
df3 = pd.read_sql('select en,jp,kotoba from difficult', 'sqlite:///ankiscore.db')
for i in df3.columns:
    globals()['df3%s' % i] = df3[i].to_list()
en,jp,koto='A','A','A'




#Test
def RanPick(mode2='N',GramVoc='V'):
    if GramVoc.upper() == 'V':
        df = 'df1'
    elif GramVoc.upper() == 'G':
        df = 'df2'
    if mode2.upper() == 'Y':
        daf = 'df3'
    else:
        daf = df
    num_prop = np.random.randint(len(globals()[daf]),size=4) #4 propositions randomly selected
    answer = np.random.randint(len(globals()[daf]),size=1)[0]
    prop = list(np.append(num_prop,answer)) #Append random propositions with the true answer 
    random.shuffle(prop) #Shuffle propositions
    return answer, prop, daf

def Convert(mode,prop,daf):
    if mode.upper() == 'J':
        outpu = 'en'
    elif mode.upper() == 'E': 
        outpu = 'jp'
    propOUT=[globals()[daf+outpu][x] for x in prop]
    #propOUT = [daf[outpu].iloc[x] for x in prop]
    return propOUT

def Question(mode,answer,daf):
    if mode.upper() == 'J':
        inpu = 'jp'
    elif mode.upper() == 'E': 
        inpu = 'en'
    question = globals()[daf+inpu][answer]
    return question, inpu

def Check(mode,choice,answer,daf,count,score,propositions):
    global en,jp,koto
    if mode.upper() == 'J':
        outpu = 'en'
    elif mode.upper() == 'E': 
        outpu = 'jp'
    if propositions[int(choice)] == globals()[daf+outpu][answer]:
        result = True
        score += 1
        count += 1
    else:
        result = False
        count += 1
        en = globals()[daf+'en'][answer]
        jp = globals()[daf+'jp'][answer]
        koto = globals()[daf+'kotoba'][answer]
    phonetic = globals()[daf+'kotoba'][answer]
    correct = globals()[daf+outpu][answer]
    return result,outpu,phonetic,correct,count,score,en,jp,koto

