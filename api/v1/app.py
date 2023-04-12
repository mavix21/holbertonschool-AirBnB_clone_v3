#!/usr/bin/python3
""" This module starts a Flask Web application that listens on 0.0.0.0
    (all network interfaces) and port 5000
"""
from os import environ
from flask import Flask, Blueprint
from models import storage
from .views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(self):
    """Removes the current session"""
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = environ.get("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = environ.get("HBNB_API_PORT", 5000)
    try:
        app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
    except Exception as e:
        print("Error: {}".format(str(e)))
