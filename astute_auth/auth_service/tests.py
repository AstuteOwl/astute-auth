from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
class AuthTestCase(APITestCase):
    def test_auth_200(self):
        resp = self.client.get('/auth/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_auth_401(self):
        resp = self.client.get('/noauth/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)