#!/usr/bin/python3
"""holds the routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects in storage"""
    amenities = [each.to_dict() for each in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object in storage"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object in storage"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """Creates a Amenity object in storage"""
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    if 'name' not in data.keys():
        return "Missing name\n", 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object in storage"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception as e:
        return "Not a JSON\n", 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
