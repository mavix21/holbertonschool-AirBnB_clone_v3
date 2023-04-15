#!/usr/bin/python3
"""This module defines the routes for users"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def show_users():
    """retrieves the list of users in storage"""
    user_objs = storage.all(User).values()
    JSON_users = [user.to_dict() for user in user_objs]

    return jsonify(JSON_users)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["GET"])
def show_user_by_id(user_id):
    searched_user = storage.get(User, user_id)
    if not searched_user:
        abort(404)

    return jsonify(searched_user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    searched_user = storage.get(User, user_id)
    if not searched_user:
        abort(404)

    searched_user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/users/", methods=["POST"])
def create_user():
    user_data = request.get_json(silent=True)
    if not user_data:
        return abort(400, description="Not a JSON")

    if "name" not in user_data:
        return abort(400, description="Missing name")

    if "password" not in user_data:
        return abort(400, desctiption="Missing password")

    new_user = User(**user_data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    searched_user = storage.get(User, user_id)
    if not searched_user:
        abort(404)

    user_data = request.get_json(silent=True)
    if not user_data:
        return abort(400, description="Not a JSON")

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in user_data.items():
        if key not in ignored_keys:
            setattr(searched_user, key, value)

    searched_user.save()

    return jsonify(searched_user.to_dict()), 200
