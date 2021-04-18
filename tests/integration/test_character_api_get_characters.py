import unittest
import requests
import json

class TestGetCharacters(unittest.TestCase):
    BASE_URL = 'http://localhost:8080'

    def setUp(self):
        self.API_URL = self.BASE_URL + '/character'

    def test_get_characters_sunny_day(self):
        response = requests.get(self.API_URL)

        # check response code and content
        self.assertIsNotNone(response)
        self.assertTrue(response.status_code == 200)

        body = response.json()
        self.assertIsNotNone(body)
        self.assertTrue(len(body) > 0)

if __name__ == '__main__':
    unittest.main()
