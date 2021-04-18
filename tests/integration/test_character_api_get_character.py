import unittest
import requests
import json

class TestGetCharacter(unittest.TestCase):
    BASE_URL = 'http://localhost:8080'

    def setUp(self):
        self.API_URL = self.BASE_URL + '/character'
        self.CHARACTER_ID = '1009144'
        self.TARGET_LANGUAGE_CODE = 'de'

    def test_get_character_sunny_day(self):
        response = requests.get(self.API_URL + '/' + self.CHARACTER_ID)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 200)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['id'])
        self.assertIsNotNone(body['name'])
        self.assertIsNotNone(body['description'])
        self.assertIsNotNone(body['thumbnail'])
        self.assertIsNotNone(body['thumbnail']['path'])
        self.assertIsNotNone(body['thumbnail']['extension'])
    
    def test_get_character_rainy_day(self):
        response = requests.get(self.API_URL + '/' + '0000000')

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 404)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['error'])
        self.assertTrue(body['error'] == 'Not found')

    def test_get_character_with_translation_sunny_day(self):
        response = requests.get(self.API_URL + '/' + self.CHARACTER_ID + '?language=' + self.TARGET_LANGUAGE_CODE)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 200)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['id'])
        self.assertIsNotNone(body['name'])
        self.assertIsNotNone(body['description'])
        self.assertIsNotNone(body['thumbnail'])
        self.assertIsNotNone(body['thumbnail']['path'])
        self.assertIsNotNone(body['thumbnail']['extension'])

    def test_get_character_with_translation_rainy_day(self):
        response = requests.get(self.API_URL + '/' + self.CHARACTER_ID + '?language=')

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 200)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertIsNotNone(body['id'])
        self.assertIsNotNone(body['name'])
        self.assertIsNotNone(body['description'])
        self.assertIsNotNone(body['thumbnail'])
        self.assertIsNotNone(body['thumbnail']['path'])
        self.assertIsNotNone(body['thumbnail']['extension'])

if __name__ == '__main__':
    unittest.main()
