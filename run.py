# -*- encoding: utf-8 -*-
import os

from flask import Flask


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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # route handles live flight traffic 
    @app.route('/page1')
    def page1():
        return 'not implemented'

    # route handles flight ticket searching 
    @app.route('/page2')
    def page2():
        return 'not implemented'

    # route handles airport routes
    @app.route('/page3')
    def page3():
        return 'not implemented'

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
