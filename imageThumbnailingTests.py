from imageThumbnailingApp import app
import unittest

class TestimageThumbnailingRoutes(unittest.TestCase):

    def testThumnails(self):
        with app.test_client() as c:
            rv = c.get('/thumbnails/42')
            body = rv.get()
            self.assertEqual(body,'<img src="thumbnails/42.jpg">')

    def testImageList(self):
        with app.test_client() as c:
            rv = c.get('/images')
            json_data = rv.get_json()
            self.assertEqual(len(json_data),20)