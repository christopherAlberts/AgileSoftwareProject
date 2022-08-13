from amadeus import ResponseError
from flask import Blueprint
from . import amadeus, cursor
from flask import request
import json

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/direct-destinations', methods=['GET'])
def direct_destinations():
    origin = request.args.get('origin')
    max = request.args.get('max')

    destinations = amadeus.airport.direct_destinations.get(departureAirportCode=origin, max=max)
    enhanced_destinations = []

    for destination in destinations.data:
        code = (destination["iataCode"])
        results = [a for a in cursor.execute(f"""
                                                        SELECT
                                                            iata_code,
                                                            name,
                                                            city,
                                                            country,
                                                            lat_decimal,
                                                            lon_decimal
                                                        FROM airports WHERE iata_code =:code LIMIT 1""", {"code": code})]
        if len(results) > 0 :
            enhanced_destinations.append(
                {
                    "id": results[0][0],
                    "title": results[0][1],
                    "geometry": { "type": "Point", "coordinates": [results[0][4], results[0][5]] }
                }
            )
    
    return json.dumps(enhanced_destinations), 200


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
    api_base = 'https://airlabs.co/api/v9/flights?_view=array&_fields=flight_icao,dir,alt,lat,lng&api_key=4544a3e6-d52c-476c-b565-0b0b22fcd05a'
    api_result = requests.get(api_base)
    api_response = api_result.json()
    return render_template('flight_traking.html', api_response = json.dumps(api_response))
