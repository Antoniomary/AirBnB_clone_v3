#!/usr/bin/python3
"""holds the routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states(state_id=None):
    """Retrieves a State object or the list of all
       State objects in storage
    """
    if state_id is not None:
        state = storage.get("State", state_id)
        if state:
            return jsonify(state.to_dict())
        abort(404)
    else:
        states = [state.to_dict() for state in storage.all("State").values()]
        return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object in storage"""
    state = storage.get("State", state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def create_state():
    """Creates a State object in storage"""
    data = request.get_json()
    if not data:
        return "Not a JSON", 400
    if 'name' not in data.keys():
        return "Missing name", 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """Updates a State object in storage"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return "Not a JSON\n", 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())
