from flask import Blueprint
from . import amadeus, cursor
from flask import request
import json

bluprint = Blueprint('api', __name__, url_prefix='/api')

@bluprint.route('/direct-destinations', methods=['GET'])
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
