from collections import OrderedDict
from flask import Flask, jsonify
from geopy.distance import vincenty

app = Flask(__name__)


# Function to get the information from a CSV file
def listStreetLightPoles(lt, ln, dt):
    path = "Montreal_StreetLigthPoles.csv"

    with open(path, 'r') as toj:
        streetLightPoles = [{'Lat': float(da.split(',')[0][1:]), 'Lon': float(da.split(',')[1][1:]),
                             'Distance': vincenty((lt, ln), (da.split(',')[0][1:], da.split(',')[1][1:])).meters} for da
                            in
                            toj if str(vincenty((lt, ln), (da.split(',')[0][1:], da.split(',')[1][1:])).meters) < dt]

    return streetLightPoles


# The url must have 5 parameters city, street, latitude, longitude, distance
@app.route('/<city>/<street>/<latitude>/<longitude>/<distance>/', methods=['GET'])
def index(city, street, latitude, longitude, distance):
    retObj = OrderedDict({
        'City': city,
        'Street': street,
        'Coordinates': {
            'Lat': float(latitude),
            'Lon': float(longitude)
        },
        'Distance': distance,
        'Distance_Unit': "meters",
        'FireHydrants': listStreetLightPoles(latitude, longitude, distance)
    })
    return jsonify(retObj)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)