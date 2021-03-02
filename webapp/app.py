import os
import csv
import requests
import json
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import joblib

#################################################
# Flask Setup
#################################################

app = Flask(__name__)
app.config.update(
    DEBUG=True,
)

#################################################
# Database Setup
#################################################
# setup mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/perfumes_db"
# app.config["MONGO_URI"] = "mongodb+srv://<dbName>:<password>@cluster0.s0gp3.mongodb.net/rescue_angels_db?retryWrites=true&w=majority"

mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find_your_scent")
def find_your_scent():
    return render_template("find_your_scent.html")


@app.route("/perfume_notes")
def pefume_notes():
    perfume_notes = list(mongo.db.perfume_notes.find({}, {'_id': False}))
    print(perfume_notes)
    return jsonify(perfume_notes)

# # testing coding form


# @app.route("perfume_form_test", methods=["POST", "GET"])
# def perfume_form_test():
#     age = str(request.form['top'])

# # user input list
#     features = [xxxxx, xxxxx, xxxxx, xxxxx, xxxx, xxxxx, xxxxxxx, xxxxx]
#     final_features = [np.array(features)]
#     final_shape = np.reshape(final_features, (1, -1))
# # load model
#     model = load("placeholder")
#     prediction = model.predict(final_shape)
# #to decide on output page ...
#     if prediction == 1:
#         return render_template("placeholder.html")
#     else:
#         return render_template("placeholder.html")


@app.route("/perfume_popularity/<featuresList>")
def perfume_popularity(featuresList):
    perfume_model = joblib.load("static/Resources/perfume_model.sav")
    outcome = perfume_model.predict(featuresList)
    return jsonify(outcome)


@app.route("/perfume_info")
def perfume_info():
    return render_template("perfume_info.html")


@app.route("/visualizations")
def visualizations():
    return render_template("visualizations.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
