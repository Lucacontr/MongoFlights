import json
from bson.json_util import loads
from bson.errors import BSONError
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


@app.route('/query')
def query():  # put application's code here
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

    return render_template("airports.html", airports=airports, airports_size=len(airports))


@app.route("/airlines")
def airlines():
    airlines = list(airlines_collection.find())

    return render_template("airlines.html", airlines=airlines, airlines_size=len(airlines))


@app.route('/insertFlight', methods=['POST'])
def insertFlight():

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

    if len(flights) == 0:
        return render_template("departure.html", message="No flights matched the given parameters")
    else:
        return render_template("departure.html", flights=flights, flights_size=len(flights))


@app.route('/queryFlights', methods=['POST'])
def queryFlights():
    query = request.form.get("Query").__str__()
    try:
        parsed_query = loads(query)
    except (BSONError, ValueError) as e:
        print('Invalid query:', e)
        return render_template("query.html", message="Invalid Query")
    else:
        if flights_collection.count_documents(parsed_query) == 0:
            return render_template("query.html", message="No document match the given query")
        else:
            result = list(flights_collection.find(parsed_query))
            if len(result) > 100:
                result = result[0:299]
            return render_template("query.html", flights=result, flights_size=len(result))

@app.route('/queryAirports', methods=['POST'])
def queryAirports():
    query = request.form.get("Query").__str__()
    try:
        parsed_query = loads(query)
    except (BSONError, ValueError) as e:
        print('Invalid query:', e)
        return render_template("query.html", message="Invalid Query")
    else:
        if airports_collection.count_documents(parsed_query) == 0:
            return render_template("query.html", message="No document match the given query")
        else:
            result = list(airports_collection.find(parsed_query))
            if len(result) > 100:
                result = result[0:299]
            return render_template("query.html", airports=result, airports_size=len(result))

@app.route('/queryAirlines', methods=['POST'])
def queryAirlines():
    query = request.form.get("Query").__str__()
    try:
        parsed_query = loads(query)
    except (BSONError, ValueError) as e:
        print('Invalid query:', e)
        return render_template("query.html", message="Invalid Query")
    else:
        if airlines_collection.count_documents(parsed_query) == 0:
            return render_template("query.html", message="No document match the given query")
        else:
            result = list(airlines_collection.find(parsed_query))
            if len(result) > 100:
                result = result[0:299]
            return render_template("query.html", airlines=result, airlines_size=len(result))


@app.route('/deleteFlight', methods=['POST'])
def deleteFlight():
    query = request.form.get("query").__str__()
    try:
        parsed_query = loads(query)
    except (BSONError, ValueError) as e:
        print('Invalid query:', e)
        return render_template("delete.html", message="Invalid Query")
    else:
        # Perform a sample find operation to validate the query
        result = flights_collection.delete_many(parsed_query)
        if result.deleted_count == 0:
            return render_template("delete.html", message="No document match the given query")
        else:
            return render_template("delete.html", message="Document deleted successfully")

@app.route('/deleteAirport', methods=['POST'])
def deleteAirport():
    query = request.form.get("query").__str__()
    try:
        parsed_query = loads(query)
    except (BSONError, ValueError) as e:
        print('Invalid query:', e)
        return render_template("delete.html", message="Invalid Query")
    else:
        # Perform a sample find operation to validate the query
        result = airports_collection.delete_many(parsed_query)
        if result.deleted_count == 0:
            return render_template("delete.html", message="No document match the given query")
        else:
            return render_template("delete.html", message="Document deleted successfully")

@app.route('/deleteAirline', methods=['POST'])
def deleteAirline():
    query = request.form.get("query").__str__()
    try:
        parsed_query = loads(query)
    except (BSONError, ValueError) as e:
        print('Invalid query:', e)
        return render_template("delete.html", message="Invalid Query")
    else:
        # Perform a sample find operation to validate the query
        result = airlines_collection.delete_many(parsed_query)
        if result.deleted_count == 0:
            return render_template("delete.html", message="No document match the given query")
        else:
            return render_template("delete.html", message="Document deleted successfully")


if __name__ == '__main__':
    app.run()
