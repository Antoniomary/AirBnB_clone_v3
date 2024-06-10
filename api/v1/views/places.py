#!/usr/bin/python3
"""holds the routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object in storage"""
    place = storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object in storage"""
    place = storage.get("Place", place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """Creates a Place object in storage"""
    city = storage.get("City", city_id)
    if not city:
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
    if 'name' not in data.keys():
        return "Missing name\n", 400
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """Updates a Place object in storage"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', strict_slashes=False,
                 methods=['POST'])
def places_search():
    """Retrieves all Place objects based on the JSON in the request body
    The JSON can contain 3 optional keys:
      * states   : list of State ids
      * cities   : list of City ids
      * amenities: list of Amenity ids
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON\n", 400
    states = data.get("states")
    cities = data.get("cities")
    amenities = data.get("amenities")
    if not data or (not states and not cities and not amenities):
        places = storage.get("Place")
        return jsonify([place.to_json() for place in places])
    result = []
    if states:
        for state in states:
            result.append(state.cities.places)
        result = set(result)
    if cities:
        for city in cities:
            result.append(city.places)
        result = set(result)
    if amenities:
        for place in result[:]:
            for amenity in amenities:
                if amenity not in place.amenities:
                    result.remove(place)
                    break
    return jsonify([place.to_dict() for place in result])
