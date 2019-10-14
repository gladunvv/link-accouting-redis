import os
import unittest

from app import app
import unittest
import subprocess
import time
from redis import Redis
import redis


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        # self.redis = redis.RedisServer()

    # def tearDown(self):
    #     self.redis.stop()


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    # def test_add_links(self):
    #     response = self.app.get('/api/v1.0/visited_links')


    def test_get_links(self):
        response = self.app.get('/api/v1.0/visited_domains?from=1570989886&to=1570989888')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    

if __name__ == "__main__":
    unittest.main()
