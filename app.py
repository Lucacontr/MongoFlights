import json

import bson
from bson import ObjectId
from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)
try:
    client = pymongo.MongoClient("localhost:27017")
    db = client["FlightsDB"]
    flights_collection = db.get_collection("Flights")
    airports_collection = db.get_collection("Airports")
    airlines_collection = db.get_collection("Airlines")
except Exception as e:
    print(e.with_traceback())


@app.route('/')
def index():  # put application's code here
    return render_template("query.html")


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
    airports = list(airports_collection.find())
    for result in airports:
        print(result)

    return render_template("airports.html", airports=airports, airports_size=len(airports))


@app.route("/airlines")
def airlines():
    airlines = list(airlines_collection.find())
    for result in airlines:
        print(result)

    return render_template("airlines.html", airlines=airlines)


@app.route('/insertFlight', methods=['POST'])
def insertFlight():
    for key, value in request.form.items():
        print(f"Field: {key} - Value: {value}")

    document = {
        "YEAR": int(request.form.get("Year").__str__()),
        "MONTH": int(request.form.get("Month").__str__()),
        "DAY": int(request.form.get("Day").__str__()),
        "AIRLINE": request.form.get("IATA_CODE"),
        "ORIGIN_AIRPORT": request.form.get("Origin"),
        "DESTINATION_AIRPORT": request.form.get("Destination"),
        "AIR_TIME": int(request.form.get("Time").__str__())
    }

    flights_collection.insert_one(document)
    return render_template("insert.html")


@app.route('/insertAirport', methods=['POST'])
def insertAirport():
    for key, value in request.form.items():
        print(f"Field: {key} - Value: {value}")

    document = {
        "IATA_CODE": request.form.get("IATA_CODE"),
        "AIRPORT": request.form.get("Name"),
        "CITY": request.form.get("City"),
        "STATE": request.form.get("State"),
        "COUNTRY": request.form.get("Country")
    }

    airports_collection.insert_one(document)
    return render_template("insert.html")


@app.route('/insertAirline', methods=['POST'])
def insertAirline():
    for key, value in request.form.items():
        print(f"Field: {key} - Value: {value}")

    document = {
        "IATA_CODE": request.form.get("IATA_CODE"),
        "AIRLINE": request.form.get("Name")
    }

    airlines_collection.insert_one(document)
    return render_template("insert.html")


@app.route('/departureSearch', methods=['POST'])
def departureSearch():

    arrayAnd = []

    if request.form.get("Year") != "":
        arrayAnd.append({"YEAR": int(request.form.get("Year").__str__())})
    if request.form.get("Month") != "":
        arrayAnd.append({"MONTH": int(request.form.get("Month").__str__())})
    if request.form.get("Day") != "":
        arrayAnd.append({"DAY": int(request.form.get("Day").__str__())})
    if request.form.get("Origin") != "":
        arrayAnd.append({"ORIGIN_AIRPORT": request.form.get("Origin").__str__()})
    if request.form.get("Destination") != "":
        arrayAnd.append({"DESTINATION_AIRPORT": request.form.get("Destination").__str__()})

    print(arrayAnd)

    query = {'$and': arrayAnd}

    # Execute the query
    flights = list(flights_collection.find(query))
    # for document in flights:
    #     print(document)

    if len(flights) == 0:
        return render_template("departure.html", message="No flights matched the given parameters")
    else:
        return render_template("departure.html", flights=flights, flights_size=len(flights))


@app.route('/queryDB', methods=['POST'])
def queryDB():
    query = request.form.get("Query").__str__()
    flights = list(flights_collection.find(json.loads(query)))
    if len(flights) == 0:
        return render_template("query.html", message="No flights matched the given query")
    else:
        if len(flights) > 100:
            flights = flights[0:299]
        return render_template("query.html", flights=flights, flights_size=len(flights))

    return render_template("query.html")


@app.route('/deleteDocument', methods=['POST'])
def deleteDocument():

    ID = request.form.get("ID").__str__()
    if not bson.objectid.ObjectId.is_valid(ID):
        return render_template("delete.html", message="Invalid ID")
    result = flights_collection.remove({'_id': ObjectId(ID)})

    if result['n'] == 0:
        return render_template("delete.html", message="No document match the given ID")
    else:
        return render_template("delete.html", message="Document deleted successfully")

    return render_template("delete.html")


if __name__ == '__main__':
    app.run()
