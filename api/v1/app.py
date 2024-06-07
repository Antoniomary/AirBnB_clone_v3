#!/usr/bin/python3
"""a flask app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exception):
    """close each session with storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """custom 404 response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    from os import getenv
    host = getenv("HBNB_API_HOST", default='0.0.0.0')
    port = int(getenv("HBNB_API_PORT", default=5000))
    app.run(host=host, port=port, threaded=True, debug=True)
