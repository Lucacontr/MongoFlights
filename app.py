from flask import Flask, render_template, request
import pymongo
import json
from pymongo import MongoClient, InsertOne

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["Flights"]
        collection = db.get_collection("Airports")

        query = {"STATE": "AK"}
        results = collection.find(query)

        # Stampa i risultati
        # for result in results:
        #     print(result)
    except Exception as e:
        print(e)
    return render_template("index.html")

@app.route("/insert")
def insert():
    return render_template("insert.html")

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/departure")
def departure():
    return render_template("departure.html")

@app.route("/airports")
def airports():
    return render_template("airports.html")

@app.route("/airlines")
def airlines():
    return render_template("airlines.html")

if __name__ == '__main__':
    app.run()
