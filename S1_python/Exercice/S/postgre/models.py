# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 19:55:24 2020

@author: Sam
"""


from app import db

class Result(db.Model):
    __tablename__ = "LinRegResults"

    id = db.Column(db.Integer, primary_key = True)
    YearsExperience = db.Column(db.Float)
    Prediction = db.Column(db.Float)

    def __init__(self, YearsExperience, Prediction):
        self.YearsExperience = YearsExperience
        self.Prediction = Prediction