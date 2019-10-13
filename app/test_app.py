import os
import unittest

from app import app
import unittest
import subprocess
import time
from redis import Redis
import redis

class RedisTest(unittest.TestCase):
    redis = None
    redis_process = None
    PORT = 6370

    @classmethod
    def setUpClass(cls):
        # print("Creating redis instance on port {0}".format(cls.PORT))
        # cls.redis_process = subprocess.Popen(
        #     ['redis-server.exe', '--port', str(cls.PORT)])
        # time.sleep(0.1)
        cls.redis = Redis(port=cls.PORT)

    # @classmethod
    # def tearDownClass(cls):
        # print "Terminating redis instance on port {0}".format(cls.PORT)
        # cls.redis_process.terminate()
        # cls.redis_process.wait()

class BasicTests(RedisTest):

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
