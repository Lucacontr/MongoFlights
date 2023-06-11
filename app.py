from flask import Flask, render_template
import pymongo
import json
from pymongo import MongoClient, InsertOne

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["FlightsDB"]
        collection = db.get_collection("Airports")

        query = {"STATE": "AK"}
        results = collection.find(query)

        # Stampa i risultati
        for result in results:
            print(result)
    except Exception as e:
        print(e)
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
