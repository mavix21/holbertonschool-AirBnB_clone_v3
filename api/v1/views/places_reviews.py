#!/usr/bin/python3
"""This module defines the routes for app_views"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def show_place_reviews(place_id):
    """retrieves a JSON of all reviews of a specified place"""
    searched_place = storage.get(Place, place_id)
    if not searched_place:
        abort(404)

    list_of_places = searched_place.reviews

    return jsonify([place.to_dict() for place in list_of_places])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=True)
def show_review_by_id(review_id):
    """retrieves a review dictionary of a specified @review_id"""
    searched_review = storage.get(Review, review_id)
    if not searched_review:
        abort(404)

    return jsonify(searched_review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=True)
def delete_review(review_id):
    """deletes a review of a specified @review_id"""
    searched_review = storage.get(Review, review_id)
    if not searched_review:
        abort(404)

    searched_review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """creates a review linked to a place with id @place_id"""
    searched_place = storage.get(Place, place_id)
    if not searched_place:
        abort(404)

    review_data = request.get_json(silent=True)
    if not review_data:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in review_data:
        return jsonify({"error": "Missing user_id"}), 400

    user_review = storage.get(User, review_data.get("user_id"))
    if not user_review:
        abort(404)

    if "text" not in review_data:
        return jsonify({"error": "Missing text"}), 400

    new_review = Review(**review_data)
    new_review.place_id = place_id
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=True)
def update_review(review_id):
    """updates a review"""
    searched_review = storage.get(Review, review_id)
    if not searched_review:
        abort(404)

    review_data = request.get_json(silent=True)
    if not review_data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in review_data.items():
        if key not in ignored_keys:
            setattr(searched_review, key, value)

    searched_review.save()

    return jsonify(searched_review.to_dict()), 200
