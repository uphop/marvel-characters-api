import os
from dotenv import load_dotenv
import time
import hashlib
import json
import requests
import logging

load_dotenv()
logger = logging.getLogger(__name__)

'''
Wrapper for Marvel API.
'''
class MarvelApiClient:
    def __init__(self):
        # retrieve base URL, public and private keys from config
        self.base_url = os.environ.get('MARVEK_API_BASE_URL', 'http://gateway.marvel.com/v1/public')
        self.public_key = os.environ.get('MARVEL_API_PUBLIC_KEY')
        self.private_key = os.environ.get('MARVEL_API_PRIVATE_KEY')

    '''
    Retrieves all characters from Marvel.
    '''
    def get_character_chunk(self, offset, limit, modified_since):
        logger.debug('Getting characters from Marvel API.')

        # get request signature
        ts, signature = self.get_signature()

        # prepare request
        request_url = f'{self.base_url}/characters'
        logger.debug(f'Base URL: {request_url}')

        params = {
            'ts': ts, 
            'apikey': self.public_key,
            'hash': signature,
            'offset': str(offset),
            'limit': str(limit),
            'modifiedSince': modified_since
        }
        logger.debug(f'API params: {params}')

        # call Marvel API
        try:
            logger.debug('Calling API...')
            response = requests.get(request_url, params = params)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        # check status code and return result
        if response.status_code != 200:
            raise SystemExit(f'Request to Marvel API failed, status: {response.status_code}')
        
        if not response.json():
            raise SystemExit(f'Request to Marvel API failed, empty response body.')

        results = response.json()
        return results

    '''
    Signs API requests with a combination of timestamp / keys.
    '''
    def get_signature(self):
        # get current timestamp
        ts = time.time()

        # check keys
        if not self.private_key or len(self.private_key) == 0:
            raise AttributeError('Failed to generate API request signature, please check private key in environment configuration.')
        
        if not self.public_key or len(self.public_key) == 0:
            raise AttributeError('Failed to generate API request signature, please check public key in environment configuration.')

        # concat timestamp and keys as hashing input, and hash to MD5
        hash_input = str(ts) + self.private_key + self.public_key
        hash_output = hashlib.md5(hash_input.encode())

        return ts, hash_output.hexdigest()

   