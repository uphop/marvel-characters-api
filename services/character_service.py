from dotenv import load_dotenv
import logging
from services.mavel_api_client import MarvelApiClient

logger = logging.getLogger(__name__)

'''
Manages character entity.
'''
class CharacterService:
    def __init__(self):
        self.api_client = MarvelApiClient()

    def get_characters(self):
        """Return all characters
        """

        # retrieve all characters from Marvel, convert to list and return
        results = []
        results = self.api_client.get_characters()
        return results

   