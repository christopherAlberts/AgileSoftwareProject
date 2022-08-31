from flite import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_direct_destinations(client):
    response = client.get('/api/direct-destinations?origin=NRT&max=1')
    assert response.data == b'{"origin": [{"id": "NRT", "title": "NEW TOKYO INTERNATIONAL", "geometry": {"type": "Point", "coordinates": [35.765, 140.386]}, "zoomLevel": 2.74, "zoomPoint": {"latitude": 35.765, "lon_decimal": 140.386}}], "destinations": [{"id": "AKL", "title": "AUCKLAND INTERNATIONAL", "geometry": {"type": "Point", "coordinates": [174.792, -37.008]}}], "destionations_were_in_origins": ["AKL"]}'

def test_ticket_prices(client):
    response = client.get('/api/ticket-prices?originalLocation=NRT&destinationLocation=LAX&date=2022-11-01')
    assert isinstance(response.data, bytes)

def test_flight_tracking(client):
    response = client.get('/api/flight_tracking')
    assert isinstance(response.data, bytes)
