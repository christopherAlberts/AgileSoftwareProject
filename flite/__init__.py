import os

from flask import Flask
from amadeus import Client
from flask_cors import CORS

amadeus = Client(
    # client_id=os.getenv("AMADEUS_CLIENT_ID"),
    # client_secret=os.getenv("AMADEUS_CLIENT_SECRET")

    client_id = 'WpuO7TVd3Kiq3qqx2GBP02r5DUcGRtSQ',
    client_secret = 'KWjVnuVCynkGFhq8'
)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import api
    app.register_blueprint(api.blueprint)
    CORS(app)

    return app
