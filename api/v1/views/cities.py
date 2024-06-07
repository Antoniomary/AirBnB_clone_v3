#!/usr/bin/python3
"""holds the routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object in storage"""
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object in storage"""
    city = storage.get("City", city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """Creates a City object in storage"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    if 'name' not in data.keys():
        return "Missing name\n", 400
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """Updates a City object in storage"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict())
