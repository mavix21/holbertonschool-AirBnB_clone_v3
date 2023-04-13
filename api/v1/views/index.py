#!/usr/bin/python3
"""This module defines the routes for app_views"""
from flask import jsonify
from . import app_views
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route("/status", strict_slashes=False)
def show_status():
    return jsonify({"status": "OK"})
