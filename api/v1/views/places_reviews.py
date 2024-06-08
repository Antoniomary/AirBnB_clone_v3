#!/usr/bin/python3
"""holds the routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object in storage"""
    review = storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object in storage"""
    review = storage.get("Review", review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """Creates a Review object in storage"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    if 'user_id' not in data.keys():
        return "Missing user_id\n", 400
    if not storage.get("User", data['user_id']):
        abort(404)
    if 'text' not in data.keys():
        return "Missing text\n", 400
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """Updates a Review object in storage"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    for key, value in data.items():
        if key not in ['id', 'user_id',
           'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict())
