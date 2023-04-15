#!/usr/bin/python3
"""This module defines the routes for amenities"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def show_amenities():
    """retrieves the list of amenitys in storage"""
    amenity_objs = storage.all(Amenity).values()
    JSON_amenities = [amenity.to_dict() for amenity in amenity_objs]

    return jsonify(JSON_amenities)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def show_amenity_by_id(amenity_id):
    searched_amenity = storage.get(Amenity, amenity_id)
    if not searched_amenity:
        abort(404)

    return jsonify(searched_amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    searched_amenity = storage.get(Amenity, amenity_id)
    if not searched_amenity:
        abort(404)

    searched_amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities/", methods=["POST"])
def create_amenity():
    amenity_data = request.get_json(silent=True)
    if not amenity_data:
        return abort(400, description="Not a JSON")

    if "name" not in amenity_data:
        return abort(400, description="Missing name")

    new_amenity = Amenity(**amenity_data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    searched_amenity = storage.get(Amenity, amenity_id)
    if not searched_amenity:
        abort(404)

    amenity_data = request.get_json(silent=True)
    if not amenity_data:
        return abort(400, description="Not a JSON")

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in amenity_data.items():
        if key not in ignored_keys:
            setattr(searched_amenity, key, value)

    searched_amenity.save()

    return jsonify(searched_amenity.to_dict()), 200
