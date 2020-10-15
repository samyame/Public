# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:02:58 2020

@author: Sam
"""

from flask import Flask, render_template, request, make_response, jsonify
import requests 
import pandas as pd
from PIL import Image
from io import BytesIO

app = Flask(__name__)

url = 'http://restratpws.azurewebsites.net/'
networks = requests.get(url+'api/Lines/metro')
networks = list(networks.json())
for i in networks:
    globals()['%s' % str(i['shortName'])] = i

@app.route("/")
def index():
 return render_template('index.html')

@app.route("/result", methods=['POST']) 
def res():
    if request.method=='POST':
        try:
            data = dict(request.form.items())
            line = 'M'+str(data["Line"])
            stations = globals()['%s' % line]['id'] 
            response = make_response(render_template("predicted.html",prediction = stations))
        except ValueError:
            return jsonify("Please enter a number.")
        return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)