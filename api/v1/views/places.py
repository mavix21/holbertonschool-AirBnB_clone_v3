#!/usr/bin/python3
"""This module defines the routes for app_views"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def show_city_places(city_id):
    """retrieves a JSON of all places of a specified city"""
    searched_city = storage.get(City, city_id)
    if not searched_city:
        abort(404)

    list_of_places = searched_city.places

    return jsonify([place.to_dict() for place in list_of_places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=True)
def show_place_by_id(place_id):
    """retrieves a place dictionary of a specified @place_id"""
    searched_place = storage.get(Place, place_id)
    if not searched_place:
        abort(404)

    return jsonify(searched_place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=True)
def delete_place(place_id):
    """deletes a place of a specified @place_id"""
    searched_place = storage.get(Place, place_id)
    if not searched_place:
        abort(404)

    searched_place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """creates a city linked to a state with id @state_id"""
    searched_city = storage.get(City, city_id)
    if not searched_city:
        abort(404)

    place_data = request.get_json(silent=True)
    if not place_data:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in place_data:
        return jsonify({"error": "Missing user_id"}), 400

    user_place = storage.get(User, place_data.get("user_id"))
    if not user_place:
        abort(404)

    if "name" not in place_data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(**place_data)
    new_place.city_id = city_id
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=True)
def update_place(place_id):
    searched_place = storage.get(Place, place_id)
    if not searched_place:
        abort(404)

    place_data = request.get_json(silent=True)
    if not place_data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in place_data.items():
        if key not in ignored_keys:
            setattr(searched_place, key, value)

    searched_place.save()

    return jsonify(searched_place.to_dict()), 200
