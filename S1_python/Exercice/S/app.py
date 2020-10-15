from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
from sklearn.externals import joblib
import requests
import json

app = Flask(__name__)

dark_sky_api_key = "073ed950bcd367ad35e76ea60cf5511c"
ipstack_api_key ="55896dde6c19b26566166b446fe84094"

@app.route("/")
def index():

    current_location = requests.get("http://api.ipstack.com/check", params={"access_key":ipstack_api_key}).json()
    lat = current_location["latitude"]
    long = current_location["longitude"]
    dark_sky = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(dark_sky_api_key,lat,long), params={"lang":"fr"}).json()
    response = make_response(render_template("index.html",
                            forecast = dark_sky))
    return response

@app.route("/predict", methods=['POST'])
def predict():
    if request.method=='POST':
        try:
            regressor = joblib.load("./linear_regression_model.pkl")
            data = dict(request.form.items())
            years_of_experience = float(data["YearsExperience"])
            prediction = regressor.predict(years_of_experience)
            response = make_response(render_template(
            "predicted.html",
            prediction = float(prediction)
            ))
        except ValueError:
            return jsonify("Please enter a number.")
        return response


if __name__ == '__main__':
    app.run(debug=True)