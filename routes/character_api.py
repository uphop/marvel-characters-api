"""Endpoints to manage FAQ topic CRUD requests"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from services.character_service import CharacterService
import logging
logger = logging.getLogger(__name__)

# Init API blueprint
character_api = Blueprint('character_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return character_api

# Init char service
character_service = CharacterService()

@character_api.route('/character', methods=['GET'])
def get_characters():
    """Return all characters
    @return: 200: an array of all characters as a \
    flask/response object with application/json mimetype.
    """
    # Retrieve characters from data store
    characters = []
    # TODO: integrate with Marvel API
    
    # HTTP 404 Not Found
    if characters is None:
        abort(404)

    return jsonify(characters)
