from amadeus import ResponseError
from flask import Blueprint
from . import amadeus
from flask import request
import json
import sqlite3
import requests

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/direct-destinations', methods=['GET'])
def direct_destinations():
    airports_db = sqlite3.connect("global_airports_sqlite.db", check_same_thread=False)
    cursor = airports_db.cursor()

    origin = request.args.get('origin')
    max = request.args.get('max')

    destinations = amadeus.airport.direct_destinations.get(departureAirportCode=origin, max=max)
    enhanced_destinations = []
    ids = []

    for destination in destinations.data:
        code = (destination["iataCode"])
        results = [a for a in cursor.execute(f"""
                                                        SELECT
                                                            iata_code,
                                                            name,
                                                            city,
                                                            country,
                                                            lon_decimal,
                                                            lat_decimal
                                                        FROM airports WHERE iata_code =:code LIMIT 1""", {"code": code})]
        if len(results) > 0 :
            enhanced_destinations.append(
                {
                    "id": results[0][0],
                    "title": results[0][1],
                    "geometry": { "type": "Point", "coordinates": [results[0][4], results[0][5]] }
                }
            )
            ids.append(results[0][0])


    origins = [a for a in cursor.execute(f"""
                                                        SELECT
                                                            iata_code,
                                                            name,
                                                            city,
                                                            country,
                                                            lon_decimal,
                                                            lat_decimal
                                                        FROM airports WHERE iata_code =:code LIMIT 1""", {"code": origin})]
    enhanced_origin = [{ 
            "id": origins[0][0],
            "title": origins[0][1],
            "geometry": { "type": "Point", "coordinates": [origins[0][4], origins[0][5]] },
            "zoomLevel": 2.74,
            "zoomPoint": { "lon_decimal": origins[0][5], "latitude": origins[0][4]}
        }]

    repsonse = {"origin": enhanced_origin, "destinations": enhanced_destinations, "destionations_were_in_origins":ids}
    
    return json.dumps(repsonse), 200



@blueprint.route('/ticket-prices', methods=['GET'])
def ticket_prices():

    originalLocation = request.args.get('originalLocation')
    destinationLocation = request.args.get('destinationLocation')
    date = request.args.get('date')

    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode = originalLocation,
            destinationLocationCode = destinationLocation,
            departureDate = date,
            adults=1)

        # Receive data from Amadeus API
        full_json_data = response.data

        # Clean data
        cleanData = clean(full_json_data)

        # Returning the cleaned data.
        return cleanData

    except ResponseError as error:
        print(error)
        return error


def clean(jsonData):

    # Building new clean array
    price_data_arr = []

    for i in jsonData:

        clean_object = {
            "id": i["id"],
            "numberOfBookableSeats": i["numberOfBookableSeats"],
            "currency": i["price"]["currency"],
            "total": i["price"]["total"],
            "base": i["price"]["base"],
            "currency": i["price"]["currency"],
            "cabin": i["travelerPricings"][0]["fareDetailsBySegment"][0]["cabin"]
            # "additionalServices" : i["price"]["additionalServices"]
        }

        price_data_arr.append(clean_object)

    # Building new clean data object.
    cleanData = {
        "num_of_entries":len(jsonData),
        "price_data" : price_data_arr
    }

    return cleanData

@blueprint.route('/flight_tracking', methods=['GET'])
def flight_tracking():
    Data = []
    api_base = 'https://opensky-network.org/api/states/all'
    api_result = requests.get(api_base)
    api_response = api_result.json()
    for i in api_response["states"]:
        val = {
        "Flight": i[1].strip(),
        "longitude": i[5], 
        "latitude" : i[6]
        }
        Data.append(val)
    return json.dumps(Data)


# Use this function if opensky api return 502 Bad Gateway

#@blueprint.route('/flight_tracking', methods=['GET'])
#def flight_tracking():
#    Data = []
#    api_base = 'https://airlabs.co/api/v9/flights?_view=array&_fields=flight_icao,lat,lng&api_key=4cd4f95a-451c-4f43-9dc1-bef9e1251b56'
#    api_result = requests.get(api_base)
#    api_response = api_result.json()
#    for i in api_response:
#        val = {
#        "Flight": i[0],
#        "latitude" : i[1],
#        "longitude": i[2]
#        }
#        Data.append(val)
#    return json.dumps(Data)

