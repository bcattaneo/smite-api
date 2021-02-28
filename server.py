import flask
from smite.api import SmiteAPI
from datetime import datetime
from flask import request, jsonify, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import *

# Flask setup
api = flask.Flask(__name__)
api.config["DEBUG"] = DEBUG
limiter = Limiter(api, key_func=get_remote_address)
CORS(api) # allow cross-origin

# Smite API handler
api_handler = None

@api.route(BASE_ENDPOINT + 'status', methods=['GET'])
@limiter.limit("1/second")
def status():
    """Return a JSON response

    Create and handle a "status" endpoint
    """

    return jsonify({ "version": SERVER_VERSION })

@api.route(BASE_ENDPOINT + '<path:path>', methods=['GET'])
@limiter.limit("1/second")
def generic_endpoint(path):
    """Return a JSON response

    Create and handle a dynamic Smite API endpoint
    with parameters
    """

    # Get method and parameters
    path_list = path.split('/')
    method = path_list[0]
    params = path_list[1:]

    # Return server response
    res = api_handler.call_generic_method(method, params)

    return jsonify(res)

def run_server():
    """Run flask server"""

    global api_handler

    # Create handler for Smite API
    api_handler = SmiteAPI(DEV_ID, AUTH_KEY, SMITE_API_URL, RESPONSE_TYPE, PLATFORM, LANGUAGE)

    # Create thread to update session token every 15 minutes
    api_handler.create_session_token_thread()

    # Start flask app
    api.run(host=SERVER_HOST, port=SERVER_PORT, threaded=True, use_reloader=False)

if __name__ == "__main__":
    run_server()