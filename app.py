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
    return render_template("airports.html")

@app.route("/airlines")
def airlines():
    return render_template("airlines.html")

@app.route('/insertFlight', methods=['POST'])
def insertFlight():
    for key, value in request.form.items():
        print(f"Field: {key} - Value: {value}")


    try:
        client = pymongo.MongoClient("localhost:27017")
        db = client["Flights"]
        collection = db.get_collection("Flights")

        documento = {
            "YEAR": request.form.get("YEAR"),
            "MONTH": request.form.get("MONTH"),
            "DAY": request.form.get("DAY"),
            "AIRLINE": request.form.get("IATA_CODE"),
            "ORIGIN_AIRPORT": request.form.get("Origin"),
            "DESTINATION_AIRPORT": request.form.get("Destination"),
            "AIR_TIME": request.form.get("Time")
        }

        inserimento = collection.insert_one(documento)
        print(inserimento)
    except Exception as e:
        print(e)
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

if __name__ == '__main__':
    app.run()
