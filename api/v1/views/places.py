#!/usr/bin/python3
"""This module defines the routes for app_views"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


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
                 strict_slashes=False)
def show_place_by_id(place_id):
    """retrieves a place dictionary of a specified @place_id"""
    searched_place = storage.get(Place, place_id)
    if not searched_place:
        abort(404)

    return jsonify(searched_place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
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
                 strict_slashes=False)
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


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def places_search():
    """retrieves all Place objects depending of the JSON in the body of the
    request."""

    search_data = request.get_json()
    if search_data is None:
        abort(400, description="Not a JSON")

    if not search_data:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    states = search_data.get("states", [])
    cities = search_data.get("cities", [])
    amenities = search_data.get("amenities", [])

    # Get all places related to states
    places_list = []
    cities_searched = []
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                cities_searched.append(city)
                places_list += city.places

    # Get all places related to cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city and city not in cities_searched:
            cities_searched.append(city)
            places_list += city.places

    if (not states and not cities) or not places_list:
        places_list = storage.all(Place).values()

    amenities_obj = [storage.get(Amenity, am_id) for am_id in amenities]
    places_list = [place for place in places_list
                   if all([amenity in place.amenities
                           for amenity in amenities_obj])]

    places_dicts = [place.to_dict().pop('amenities', None)
                    for place in places_list]

    return jsonify(places_dicts)
