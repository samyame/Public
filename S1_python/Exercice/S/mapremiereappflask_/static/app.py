from flask import Flask, render_template, request
import datetime
import pandas as pd
#import numpy

app = Flask(__name__)


@app.route("/homepage")
def index():
 return render_template('homepage.html')

import requests
key = '55896dde6c19b26566166b446fe84094'
url ='http://api.ipstack.com/check'
request = requests.get(url, params = {'access_key':key}).json()

coord = [request['latitude'],request['longitude']]

met = 'https://api.darksky.net/forecast/'
key2 = '073ed950bcd367ad35e76ea60cf5511c/'
meteo = requests.get(met+key2+str(coord[0])+','+str(coord[1])).json()

final = pd.DataFrame(index = meteo['currently'].keys(), data = meteo['currently'].values())
final.to_html('test.html')

@app.route('/reponse')
def result():
   return render_template("reponse.html")


if __name__ == '__main__':
    app.run(debug=True)
