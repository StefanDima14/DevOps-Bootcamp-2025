import unittest
from hello_world import app

class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_hello_world(self):
        response = self.app.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"data": "Hello World"})

if __name__ == '__main__':
    unittest.main()
