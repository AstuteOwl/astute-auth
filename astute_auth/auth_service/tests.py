from django.test import TestCase


# Create your tests here.
class AuthTestCase(TestCase):
    def test_auth_200(self):
        resp = self.client.get('/auth/')
        self.assertEqual(resp.status_code, 200)

    def test_no_auth_400(self):
        resp = self.client.get('/noauth/')
        self.assertEqual(resp.status_code, 401)