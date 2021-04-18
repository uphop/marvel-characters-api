import os
from datetime import datetime
from dotenv import load_dotenv
import logging
from services.mavel_api_client import MarvelApiClient
from data.datastores.character_data_store import CharacterDataStore
from services.aws_translate_api_client import AwsTranslateApiClient

logger = logging.getLogger(__name__)
load_dotenv()

'''
Manages character entity.
'''
class CharacterService:
    def __init__(self):
        self.marvel_api = MarvelApiClient()
        self.data_store = CharacterDataStore()
        self.translate_api = AwsTranslateApiClient()

    def get_characters(self):
        """Return all characters
        """
        # retrieve all character IDs
        results = self.data_store.get_characters()
        return [id for id, in results] if not results is None else []

    def get_character_by_id(self, id, target_language_code=None):
        """Return all characters
        """
        # retrieve character details
        result = self.data_store.get_character_by_id(id)
        if not result is None:
            # map data tsore result
            character = {
                'id': result.id,
                'name': result.name,
                'description': result.description,
                'thumbnail': {
                    'path': result.thumbnail_path,
                    'extension': result.thumbnail_extension,
                }
            }

            # if translation is needed - translate description
            if not target_language_code is None and len(target_language_code) == 2:
                source_language_code = os.environ.get('AWS_SOURCE_LANGUAGE_CODE', 'en')
                character['description'] = self.translate_api.translate(
                    source_language_code=source_language_code, 
                    target_language_code=target_language_code, 
                    text=result.description)

            return character

    def sync(self):
        logger.debug('Synching characters...')
        
        # check if characters already synced
        modified_start_of_time = '1901-01-01T00:00:00-0000'
        character_last_modified = self.data_store.get_character_last_modified()
        modified_since = character_last_modified.modified if not character_last_modified is None else modified_start_of_time
        logger.debug(f'Characters modified since: {modified_since}')

        # init chunk 
        offset = 0
        limit = os.environ.get('MARVEL_API_LIMIT', '100')

        # get chunks of characters in a loop
        while True:
            # get next character chunk
            chunk = self.marvel_api.get_character_chunk(offset=offset, limit=limit, modified_since=modified_since)

            # iterate through the chunk and add characters to data store
            data = chunk['data']
            characters = data['results']

            # some modifed values returned from Marvel are of incorrect format
            # assumed the date/time can be set to the start of time
            modified_invalid_format = '-0001-11-30T00:00:00-0500'
            
            for character in characters:
                try:
                    # check if character already exists
                    existing_character = self.data_store.get_character_by_id(character['id'])
                    if not existing_character is None:
                        # update existing character
                        self.data_store.update_character(
                            id=character['id'], 
                            name=character['name'], 
                            description=character['description'], 
                            modified=datetime.strptime(character['modified'].replace(modified_invalid_format, modified_start_of_time), '%Y-%m-%dT%H:%M:%S%z'),
                            thumbnail_path=character['thumbnail']['path'],
                            thumbnail_extension=character['thumbnail']['extension'])
                    else:
                        # add character to data store
                        self.data_store.create_character(
                            id=character['id'], 
                            name=character['name'], 
                            description=character['description'], 
                            modified=datetime.strptime(character['modified'].replace(modified_invalid_format, modified_start_of_time), '%Y-%m-%dT%H:%M:%S%z'),
                            thumbnail_path=character['thumbnail']['path'],
                            thumbnail_extension=character['thumbnail']['extension'])
                except Exception as err:
                    logger.error('Failed to load character: ' + str(err))

            # target next chunk
            offset = int(data['offset'])
            total = int(data['total'])
            count = int(data['count'])

            # if no remaining characters, break out
            remaining = total - offset - count
            if remaining <= 0:
                logger.debug(f'Synching completed, total characters {total}')
                break

            offset += int(limit)

    


   