# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 13:30:48 2020

@author: Sam
"""


from flask import Flask, render_template, request, make_response
import datetime
import pandas as pd
import numpy
import requests

app = Flask(__name__)

@app.route("/")
def quest():
    

@app.route("/")
def index():
    key = '55896dde6c19b26566166b446fe84094'
    url ='http://api.ipstack.com/check'
    request = requests.get(url, params = {'access_key':key}).json()
    
    coord = [request['latitude'],request['longitude']]
    
    met = 'https://api.darksky.net/forecast/'
    key2 = '073ed950bcd367ad35e76ea60cf5511c/'
    meteo = requests.get(met+key2+str(coord[0])+','+str(coord[1]),params = {'lang':'fr'}).json()
    
    final = pd.DataFrame(index = meteo['currently'].keys(), data = meteo['currently'].values(),columns =['currently'])
    final.to_html(r'templates\test.html')
    
    response = make_response(render_template("test.html"))
    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)