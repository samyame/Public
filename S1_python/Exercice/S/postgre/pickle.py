# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:06:37 2020

@author: Sam
"""


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib


df = pd.read_csv('Salary_Data.csv')
X = df['YearsExperience'].values.reshape(-1,1)
Y = df['Salary'].values

regressor = LinearRegression()

regressor.fit(X,Y)
joblib.dump(regressor, "linear_regression_model.pkl")
