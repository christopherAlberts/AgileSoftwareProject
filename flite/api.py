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
        enhanced_destinations.extend([a for a in cursor.execute(f"""
                                                        SELECT
                                                            iata_code,
                                                            name,
                                                            city,
                                                            country,
                                                            lat_decimal,
                                                            lon_decimal
                                                        FROM airports WHERE iata_code =:code""", {"code": code})])    
    
    return json.dumps(enhanced_destinations), 200
