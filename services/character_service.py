import os
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
        characters = self.data_store.get_characters()
        if len(characters) > 0:
            return

        # init chunk 
        offset = 0
        limit = os.environ.get('MARVEL_API_LIMIT', '100')

        # get chunks of characters in a loop
        while True:
            # get next character chunk
            chunk = self.marvel_api.get_character_chunk(offset=offset, limit=limit)

            # iterate through the chunk and add characters to data store
            data = chunk['data']
            characters = data['results']
            for character in characters:
                self.data_store.create_character(
                    id=character['id'], 
                    name=character['name'], 
                    description=character['description'], 
                    modified=character['modified'], 
                    thumbnail_path=character['thumbnail']['path'],
                    thumbnail_extension=character['thumbnail']['extension'])

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

    


   