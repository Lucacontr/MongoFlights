from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
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
    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["FlightsDB"]
        collection = db.get_collection("Airports")

        airports = list(collection.find())
        for result in airports:
            print(result)

    except Exception as e:
        print(e.with_traceback())
    return render_template("airports.html", airports=airports, airports_size=len(airports))


@app.route("/airlines")
def airlines():
    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["FlightsDB"]
        collection = db.get_collection("Airlines")

        airlines = list(collection.find())
        for result in airlines:
            print(result)

    except Exception as e:
        print(e.with_traceback())
    return render_template("airlines.html", airlines=airlines)


@app.route('/insertFlight', methods=['POST'])
def insertFlight():
    for key, value in request.form.items():
        print(f"Field: {key} - Value: {value}")

    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["Flights"]
        collection = db.get_collection("Flights")

        documento = {
            "YEAR": int(request.form.get("Year").__str__()),
            "MONTH": int(request.form.get("Month").__str__()),
            "DAY": int(request.form.get("Day").__str__()),
            "AIRLINE": request.form.get("IATA_CODE"),
            "ORIGIN_AIRPORT": request.form.get("Origin"),
            "DESTINATION_AIRPORT": request.form.get("Destination"),
            "AIR_TIME": int(request.form.get("Time").__str__())
        }

        inserimento = collection.insert_one(documento)
        print(inserimento)
    except Exception as e:
        print(e.with_traceback())
    return render_template("insert.html")


@app.route('/insertAirport', methods=['POST'])
def insertAirport():
    for key, value in request.form.items():
        print(f"Field: {key} - Value: {value}")

    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["Flights"]
        collection = db.get_collection("Airports")

        documento = {
            "IATA_CODE": request.form.get("IATA_CODE"),
            "AIRPORT": request.form.get("Name"),
            "CITY": request.form.get("City"),
            "STATE": request.form.get("State"),
            "COUNTRY": request.form.get("Country")
        }

        inserimento = collection.insert_one(documento)
        print(inserimento)
    except Exception as e:
        print(e)
    return render_template("insert.html")


@app.route('/insertAirline', methods=['POST'])
def insertAirline():
    for key, value in request.form.items():
        print(f"Field: {key} - Value: {value}")

    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["Flights"]
        collection = db.get_collection("Airlines")

        documento = {
            "IATA_CODE": request.form.get("IATA_CODE"),
            "AIRLINE": request.form.get("Name")
        }

        inserimento = collection.insert_one(documento)
        print(inserimento)
    except Exception as e:
        print(e)

    return render_template("insert.html")

@app.route('/departureSearch', methods=['POST'])
def departureSearch():

    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["Flights"]
        collection = db.get_collection("Flights")
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
        result = collection.find(query)

        # Print the matching documents
        for document in result:
            print(document)
    except Exception as e:
        print(e.with_traceback())
    return render_template("departure.html")



if __name__ == '__main__':
    app.run()
