#!/usr/bin/python3
"""holds the routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object in storage"""
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object in storage"""
    user = storage.get("User", user_id)
    if user:
        user.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def create_user():
    """Creates a User object in storage"""
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    if 'email' not in data.keys():
        return "Missing email\n", 400
    if 'password' not in data.keys():
        return "Missing password\n", 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Updates a User object in storage"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    try:
        data = request.get_json()
        if not data:
            return "Not a JSON\n", 400
    except Exception:
        return "Not a JSON\n", 400
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict())
