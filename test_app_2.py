import unittest
from app import app


class TestApp2(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_sum_negative(self):
        r = self.client.post('/sum', data={'a': '-2', 'b': '-3'})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'-5.0', r.data)

    def test_sum_decimal(self):
        r = self.client.post('/sum', data={'a': '1.5', 'b': '2.5'})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'4.0', r.data)

    def test_hello_strips_spaces(self):
        r = self.client.post('/hello', data={'username': '   '})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Hello there', r.data)

    def test_unknown_route(self):
        self.assertEqual(self.client.get('/nope').status_code, 404)


if __name__ == "__main__":
    unittest.main()
