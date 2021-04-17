import os
from dotenv import load_dotenv
import logging
from services.mavel_api_client import MarvelApiClient
from data.datastores.character_data_store import CharacterDataStore

logger = logging.getLogger(__name__)
load_dotenv()

'''
Manages character entity.
'''
class CharacterService:
    def __init__(self):
        self.api_client = MarvelApiClient()
        self.data_store = CharacterDataStore()

    def get_characters(self):
        """Return all characters
        """
        # retrieve all character IDs
        results = self.data_store.get_characters()
        return [id for id, in results] if not results is None else []

    def get_character_by_id(self, id):
        """Return all characters
        """
        # retrieve character details
        result = self.data_store.get_character_by_id(id)
        if not result is None:
            character = {
                'id': result.id,
                'name': result.name,
                'description': result.description,
                'thumbnail': {
                    'path': result.thumbnail_path,
                    'extension': result.thumbnail_extension,
                }
            }
            return character

    def sync(self):
        logger.debug('Synching characters...')

        # delete exsiting characters
        self.data_store.delete_characters()

        # init chunk 
        offset = 1450
        limit = os.environ.get('MARVEL_API_LIMIT', '100')

        # get chunks of characters in a loop
        while True:
            # get next character chunk
            chunk = self.api_client.get_character_chunk(offset=offset, limit=limit)

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

    


   