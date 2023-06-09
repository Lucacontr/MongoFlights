from flask import Flask, render_template
import pymongo
import json
from pymongo import MongoClient, InsertOne

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here

    client = pymongo.MongoClient("localhost:27017")
    db = client.get_database("Flights")
    collection = db.get_collection("Flights")
    # requesting = []
    #
    # with open(r"") as f:
    #     for jsonObj in f:
    #         myDict = json.loads(jsonObj)
    #         requesting.append(InsertOne(myDict))
    #
    # result = collection.bulk_write(requesting)
    # client.close()
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
