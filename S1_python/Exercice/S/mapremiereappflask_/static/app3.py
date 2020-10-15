# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 13:30:48 2020

@author: Sam
"""


from flask import Flask, render_template, request, make_response, jsonify
import joblib
import numpy as np
import requests
import json
import os


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('quest.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method=='POST':
        regressor = joblib.load("linear_regression_model.pkl")
        data = dict(request.form.items())
        years_of_experience = float(data["YearsExperience"])
        prediction = regressor.predict(years_of_experience)
        response = make_response(render_template(
        "predicted.html",
        prediction = float(prediction)
        ))
    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)