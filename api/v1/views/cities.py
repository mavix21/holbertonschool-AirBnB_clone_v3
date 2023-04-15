#!/usr/bin/python3
"""This module defines the routes for app_views"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def show_state_cities(state_id):
    """retrieves a JSON of all cities of a specified state"""
    searched_state = storage.get(State, state_id)
    if not searched_state:
        abort(404)

    list_of_cities = searched_state.cities

    return jsonify([city.to_dict() for city in list_of_cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=True)
def show_city_by_id(city_id):
    """retrieves a city dictionary of a specified @city_id"""
    searched_city = storage.get(City, city_id)
    if not searched_city:
        abort(404)

    return jsonify(searched_city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=True)
def delete_city(city_id):
    """deletes a city of a specified @city_id"""
    searched_city = storage.get(City, city_id)
    if not searched_city:
        abort(404)

    searched_city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city linked to a state with id @state_id"""
    searched_state = storage.get(State, state_id)
    if not searched_state:
        abort(404)

    city_data = request.get_json(silent=True)
    if not city_data:
        abort(400, description="Not a JSON")

    if "name" not in city_data:
        abort(400, description="Missing name")

    # New city must be inserted with parameter state_id
    # city_data["state_id"] = searched_state.id

    # ignored_keys = ["id", "created_at", "updated_at"]

    # city_data = {k: v for k, v in city_data.items()
    #            if k not in ignored_keys}

    new_city = City(**city_data)
    new_city.state_id = state_id
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=True)
def update_city(city_id):
    searched_city = storage.get(City, city_id)
    if not searched_city:
        abort(404)

    city_data = request.get_json(silent=True)
    if not city_data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in city_data.items():
        if key not in ignored_keys:
            setattr(searched_city, key, value)

    searched_city.save()

    return jsonify(searched_city.to_dict()), 200
