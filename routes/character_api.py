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

# run initial sync
character_service.sync()

@character_api.route('/character', methods=['GET'])
def get_characters():
    """Return all characters
    @return: 200: an array of all characters as a \
    flask/response object with application/json mimetype.
    """
    # Retrieve characters from data store
    characters = character_service.get_characters()
    
    # HTTP 404 Not Found
    if characters is None:
        abort(404)

    return jsonify(characters)

@character_api.route('/character/<string:_character_id>', methods=['GET'])
def get_character_by_id(_character_id):
    """Return character by ID.
    @param _character_id: character's identifier
    @return: 200: a character as \
    flask/response object with application/json mimetype.
    @raise 400: missing required parameter
    @raise 404: if character is not found
    """
    # Retrieve character from data store
    character = character_service.get_character_by_id(_character_id)
    
    # HTTP 404 Not Found
    if character is None:
        abort(404)

    return jsonify(character)
