#!/usr/bin/python3
"""This module defines the routes for states"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def show_states():
    """retrieves the list of states in storage"""
    state_objs = storage.all(State).values()
    JSON_states = [state.to_dict() for state in state_objs]

    return jsonify(JSON_states)


@app_views.route("/states/<state_id>", methods=["GET"])
def show_state_by_id(state_id):
    searched_state = storage.get(State, state_id)
    if not searched_state:
        abort(404)

    return jsonify(searched_state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    searched_state = storage.get(State, state_id)
    if not searched_state:
        abort(404)

    searched_state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"])
def create_state():
    state_data = request.get_json(silent=True)
    if not state_data:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in state_data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**state_data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    searched_state = storage.get(State, state_id)
    if not searched_state:
        abort(404)

    state_data = request.get_json(silent=True)
    if not state_data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in state_data.items():
        if key not in ignored_keys:
            setattr(searched_state, key, value)

    searched_state.save()

    return jsonify(searched_state.to_dict()), 200
