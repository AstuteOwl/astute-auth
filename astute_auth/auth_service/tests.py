from astute_auth.auth_service.models import UserVerification
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from jwt import verify_jwt
from rest_framework.test import APITestCase
from rest_framework import status
from astute_auth import settings
import json

class TokenTestCase(APITestCase):
	email = 'myemail@domain.com'
	password = 'my_password'

	def test_no_username_or_password_400(self):
		resp = self.client.post('/token/')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_new_account(self):
		resp = self.client.post('/token/', data={'email': self.email, 'password': self.password})
		self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
		user = User.objects.get(username=self.email)
		self.assertIsNotNone(user)
		user = authenticate(username=self.email, password=self.password)
		self.assertIsNotNone(user)
		self.assertEqual(False, user.is_active)
		user_verification = UserVerification.objects.filter(email=self.email)
		self.assertIsNotNone(user_verification)

	def test_existing_account_bad_password(self):
		bad_password = "bad_password"
		# create the account
		User.objects.create_user(self.email, self.email, self.password)
		# authenticate w/bad password
		resp = self.client.post('/token/', data={'email': self.email, 'password': bad_password})
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_existing_active_account_correct_password(self):
		# create the account
		user = User.objects.create_user(self.email, self.email, self.password)
		user.is_active = True
		user.save()
		# authenticate
		resp = self.client.post('/token/', data={'email': self.email, 'password': self.password})
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		token = json.loads(resp.content)['token']
		header, claims = verify_jwt(token, settings.HMAC_SECRET, ['HS512'])
		self.assertEqual(claims['email'], self.email)
		self.assertEqual(header['alg'], u'HS512')

	def test_existing_inactive_account_correct_password(self):
		# create the inactive account
		user = User.objects.create_user(self.email, self.email, self.password)
		user.is_active = False
		user.save()
		# authenticate
		resp = self.client.post('/token/', data={'email': self.email, 'password': self.password})
		self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)


class PingTestCase(APITestCase):
	def test_ping_get(self):
		resp = self.client.get('/ping')
		self.assertEqual('pong', resp.data)